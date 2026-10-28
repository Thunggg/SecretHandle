package com.secrethandle.b3;

import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.os.Build;
import android.os.Bundle;
import android.service.notification.NotificationListenerService;
import android.service.notification.StatusBarNotification;
import android.util.Log;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * B3 broker: the notification that carries a one-time code never reaches the
 * shade in clear text.
 *
 * For every posted notification that contains a code, the broker mints a handle,
 * cancels the original notification and posts a redacted replacement. The code
 * itself stays in {@link Vault}. This mirrors the Mint step of the paper's
 * algorithm; the Resolve step is the explicit reveal in MainActivity.
 */
public class SecretBrokerService extends NotificationListenerService {

    public static final String TAG = "SHBroker";
    public static final String CHANNEL_ID = "secrethandle";

    /** Numeric OTP or the synthetic canary format used in our experiments. */
    private static final Pattern SECRET = Pattern.compile(
            "(\\bSH-[A-Z0-9]{6,10}\\b)|(\\b\\d{6,8}\\b)");

    @Override
    public void onCreate() {
        super.onCreate();
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            NotificationChannel ch = new NotificationChannel(
                    CHANNEL_ID, "SecretHandle", NotificationManager.IMPORTANCE_DEFAULT);
            ch.setDescription("Redacted notifications");
            getSystemService(NotificationManager.class).createNotificationChannel(ch);
        }
        audit("broker_started", "-", "-");
    }

    @Override
    public void onNotificationPosted(StatusBarNotification sbn) {
        try {
            if (sbn == null || sbn.getNotification() == null) {
                return;
            }
            if (getPackageName().equals(sbn.getPackageName())) {
                return;
            }
            Bundle ex = sbn.getNotification().extras;
            if (ex == null) {
                return;
            }
            String full = flatten(ex);
            String secret = extract(full);
            if (secret == null) {
                return;
            }
            String handle = Vault.mint(secret, sbn.getPackageName());
            cancelNotification(sbn.getKey());
            postRedacted(sbn.getPackageName(), handle);
            audit("mint", handle, sbn.getPackageName() + " secret_len=" + secret.length());
            Log.i(TAG, "minted " + handle + " from " + sbn.getPackageName());
        } catch (Throwable t) {
            Log.e(TAG, "onNotificationPosted", t);
        }
    }

    private void postRedacted(String source, String handle) {
        Intent i = new Intent(this, MainActivity.class);
        i.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
        PendingIntent pi = PendingIntent.getActivity(
                this, 0, i, PendingIntent.FLAG_IMMUTABLE | PendingIntent.FLAG_UPDATE_CURRENT);
        Notification.Builder b = Build.VERSION.SDK_INT >= Build.VERSION_CODES.O
                ? new Notification.Builder(this, CHANNEL_ID)
                : new Notification.Builder(this);
        Notification n = b
                .setSmallIcon(android.R.drawable.ic_lock_lock)
                .setContentTitle("SecretHandle: code protected")
                .setContentText(handle + " from " + labelFor(source) + " - open SecretHandle to use it")
                .setContentIntent(pi)
                .setAutoCancel(true)
                .build();
        getSystemService(NotificationManager.class).notify(1, n);
    }

    /** User-facing app label; falls back to the package name for unknown sources. */
    private String labelFor(String pkg) {
        try {
            android.content.pm.PackageManager pm = getPackageManager();
            android.content.pm.ApplicationInfo ai = pm.getApplicationInfo(pkg, 0);
            return pm.getApplicationLabel(ai).toString();
        } catch (Throwable t) {
            return pkg;
        }
    }

    private static String flatten(Bundle ex) {
        StringBuilder sb = new StringBuilder();
        sb.append(cs(ex.getCharSequence(Notification.EXTRA_TITLE))).append(" ");
        sb.append(cs(ex.getCharSequence(Notification.EXTRA_TEXT))).append(" ");
        sb.append(cs(ex.getCharSequence(Notification.EXTRA_BIG_TEXT))).append(" ");
        sb.append(cs(ex.getCharSequence(Notification.EXTRA_SUB_TEXT))).append(" ");
        for (String key : ex.keySet()) {
            Object v = ex.get(key);
            if (v instanceof CharSequence) {
                sb.append(cs((CharSequence) v)).append(" ");
            } else if (v instanceof CharSequence[]) {
                for (CharSequence c : (CharSequence[]) v) {
                    sb.append(cs(c)).append(" ");
                }
            }
        }
        return sb.toString().replaceAll("\\s+", " ").trim();
    }

    private static String cs(CharSequence c) {
        return c == null ? "" : c.toString();
    }

    static String extract(String s) {
        Matcher m = SECRET.matcher(s);
        while (m.find()) {
            if (m.group(1) != null) {
                return m.group(1);
            }
            if (m.group(2) != null) {
                return m.group(2);
            }
        }
        return null;
    }

    /** Append-only audit trail; readable with `adb shell run-as com.secrethandle.b3 cat files/audit.jsonl`. */
    static synchronized void audit(String event, String handle, String detail) {
        try {
            File dir = new File("/data/data/com.secrethandle.b3/files");
            if (!dir.exists()) {
                dir.mkdirs();
            }
            File f = new File(dir, "audit.jsonl");
            FileWriter w = new FileWriter(f, true);
            String ts = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSS", Locale.US)
                    .format(new Date());
            w.write("{\"ts\":\"" + ts + "\",\"event\":\"" + event + "\",\"handle\":\""
                    + handle + "\",\"detail\":\"" + detail.replace("\"", "'") + "\"}\n");
            w.close();
        } catch (IOException e) {
            Log.e(TAG, "audit failed", e);
        }
    }
}
