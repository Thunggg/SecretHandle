package com.secrethandle.b3;

import android.app.Activity;
import android.content.ClipboardManager;
import android.content.Context;
import android.os.Build;
import android.os.Bundle;
import android.security.keystore.KeyGenParameterSpec;
import android.security.keystore.KeyInfo;
import android.security.keystore.KeyProperties;
import android.util.Log;
import android.widget.TextView;

import java.io.FileOutputStream;
import java.nio.charset.StandardCharsets;
import java.security.KeyStore;
import java.util.Arrays;
import java.util.Locale;

import javax.crypto.KeyGenerator;
import javax.crypto.Mac;
import javax.crypto.SecretKey;
import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.SecretKeySpec;

/**
 * Benchmarks real hardware-backed AndroidKeyStore TEE HMAC-SHA256 operations
 * inside a full Android application context against cached in-memory HMAC-SHA256
 * and system_server Binder IPC round-trips.
 */
public class TeeBenchmarkActivity extends Activity {

    private static final String TAG = "SH_TEE_BENCH";
    private static final String KEY_ALIAS = "sh_tee_hmac_bench_v1";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        final TextView tv = new TextView(this);
        tv.setTextSize(12);
        tv.setText("Running AndroidKeyStore TEE benchmark...");
        setContentView(tv);

        new Thread(new Runnable() {
            @Override
            public void run() {
                final String json = executeBenchmark();
                Log.i(TAG, json);
                try {
                    FileOutputStream fos = openFileOutput("tee_benchmark.json", Context.MODE_PRIVATE);
                    fos.write(json.getBytes(StandardCharsets.UTF_8));
                    fos.close();
                } catch (Exception e) {
                    Log.e(TAG, "Failed writing json", e);
                }
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        tv.setText(json);
                    }
                });
            }
        }).start();
    }

    private String executeBenchmark() {
        try {
            KeyStore ks = KeyStore.getInstance("AndroidKeyStore");
            ks.load(null);
            if (!ks.containsAlias(KEY_ALIAS)) {
                KeyGenerator kg = KeyGenerator.getInstance(
                        KeyProperties.KEY_ALGORITHM_HMAC_SHA256, "AndroidKeyStore");
                kg.init(new KeyGenParameterSpec.Builder(
                        KEY_ALIAS, KeyProperties.PURPOSE_SIGN)
                        .setDigests(KeyProperties.DIGEST_SHA256)
                        .build());
                kg.generateKey();
            }

            SecretKey teeKey = (SecretKey) ks.getKey(KEY_ALIAS, null);
            SecretKeyFactory factory = SecretKeyFactory.getInstance(
                    teeKey.getAlgorithm(), "AndroidKeyStore");
            KeyInfo info = (KeyInfo) factory.getKeySpec(teeKey, KeyInfo.class);
            boolean insideSecureHw = info.isInsideSecureHardware();
            int secLevel = (Build.VERSION.SDK_INT >= 31) ? info.getSecurityLevel() : -1;
            String secLabel = securityLevelName(secLevel, insideSecureHw);

            byte[] payload = "SH-A8F29C|com.legitimate.bank|otp_input|task42"
                    .getBytes(StandardCharsets.UTF_8);

            // Warmup TEE keystore2/KeyMint path
            for (int i = 0; i < 5; i++) {
                Mac mac = Mac.getInstance("HmacSHA256");
                mac.init(teeKey);
                mac.doFinal(payload);
            }

            final int teeN = 100;
            long[] teeInitDoFinalNs = new long[teeN];
            for (int i = 0; i < teeN; i++) {
                long t0 = System.nanoTime();
                Mac mac = Mac.getInstance("HmacSHA256");
                mac.init(teeKey);
                mac.doFinal(payload);
                teeInitDoFinalNs[i] = System.nanoTime() - t0;
            }

            // Also measure pre-initialized Mac + TEE doFinal
            long[] teeDoFinalOnlyNs = new long[teeN];
            for (int i = 0; i < teeN; i++) {
                Mac mac = Mac.getInstance("HmacSHA256");
                mac.init(teeKey);
                long t0 = System.nanoTime();
                mac.doFinal(payload);
                teeDoFinalOnlyNs[i] = System.nanoTime() - t0;
            }

            // Cached in-memory SecretKeySpec (same session-key caching pattern as BenchmarkRunner)
            byte[] rawSessionKey = new byte[32];
            for (int i = 0; i < 32; i++) {
                rawSessionKey[i] = (byte) (0x41 + i);
            }
            SecretKeySpec ramKey = new SecretKeySpec(rawSessionKey, "HmacSHA256");
            for (int i = 0; i < 100; i++) {
                Mac mac = Mac.getInstance("HmacSHA256");
                mac.init(ramKey);
                mac.doFinal(payload);
            }
            final int ramN = 1000;
            long[] ramNs = new long[ramN];
            for (int i = 0; i < ramN; i++) {
                long t0 = System.nanoTime();
                Mac mac = Mac.getInstance("HmacSHA256");
                mac.init(ramKey);
                mac.doFinal(payload);
                ramNs[i] = System.nanoTime() - t0;
            }

            // Cross-process Binder IPC baseline to system_server (PackageManager / Clipboard)
            final int ipcN = 100;
            long[] binderNs = new long[ipcN];
            ClipboardManager cm = (ClipboardManager) getSystemService(Context.CLIPBOARD_SERVICE);
            for (int i = 0; i < 5; i++) {
                cm.hasPrimaryClip();
            }
            for (int i = 0; i < ipcN; i++) {
                long t0 = System.nanoTime();
                cm.hasPrimaryClip();
                binderNs[i] = System.nanoTime() - t0;
            }

            return String.format(Locale.US,
                    "{\"device_model\":\"%s\",\"android_release\":\"%s\",\"api_level\":%d,"
                    + "\"keystore_provider\":\"AndroidKeyStore\","
                    + "\"inside_secure_hardware\":%s,"
                    + "\"security_level_code\":%d,"
                    + "\"security_level_label\":\"%s\","
                    + "\"tee_trials\":%d,"
                    + "\"tee_hmac_init_dofinal_us\":%s,"
                    + "\"tee_hmac_dofinal_only_us\":%s,"
                    + "\"ram_session_trials\":%d,"
                    + "\"ram_session_hmac_us\":%s,"
                    + "\"binder_ipc_trials\":%d,"
                    + "\"system_binder_ipc_us\":%s}",
                    escape(Build.MODEL),
                    escape(Build.VERSION.RELEASE),
                    Build.VERSION.SDK_INT,
                    insideSecureHw ? "true" : "false",
                    secLevel,
                    secLabel,
                    teeN,
                    statsUs(teeInitDoFinalNs),
                    statsUs(teeDoFinalOnlyNs),
                    ramN,
                    statsUs(ramNs),
                    ipcN,
                    statsUs(binderNs));
        } catch (Exception e) {
            return "{\"error\":\"" + escape(e.toString()) + "\"}";
        }
    }

    private static String securityLevelName(int code, boolean insideSecureHw) {
        if (Build.VERSION.SDK_INT >= 31) {
            if (code == KeyProperties.SECURITY_LEVEL_TRUSTED_ENVIRONMENT) {
                return "SECURITY_LEVEL_TRUSTED_ENVIRONMENT";
            }
            if (code == KeyProperties.SECURITY_LEVEL_STRONGBOX) {
                return "SECURITY_LEVEL_STRONGBOX";
            }
            if (code == KeyProperties.SECURITY_LEVEL_SOFTWARE) {
                return "SECURITY_LEVEL_SOFTWARE";
            }
            return "UNKNOWN_" + code;
        }
        return insideSecureHw ? "INSIDE_SECURE_HARDWARE" : "SOFTWARE";
    }

    private static String statsUs(long[] samples) {
        long[] s = Arrays.copyOf(samples, samples.length);
        Arrays.sort(s);
        double sum = 0.0;
        for (long v : s) {
            sum += v;
        }
        double median = s[s.length / 2] / 1000.0;
        double p95 = s[(int) Math.min(s.length - 1, Math.floor(s.length * 0.95))] / 1000.0;
        double mean = (sum / s.length) / 1000.0;
        double min = s[0] / 1000.0;
        double max = s[s.length - 1] / 1000.0;
        return String.format(Locale.US,
                "{\"median\":%.2f,\"p95\":%.2f,\"mean\":%.2f,\"min\":%.2f,\"max\":%.2f}",
                median, p95, mean, min, max);
    }

    private static String escape(String s) {
        return s == null ? "" : s.replace("\\", "\\\\").replace("\"", "\\\"");
    }
}
