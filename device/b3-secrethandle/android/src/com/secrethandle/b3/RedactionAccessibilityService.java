package com.secrethandle.b3;

import android.accessibilityservice.AccessibilityService;
import android.graphics.PixelFormat;
import android.graphics.Rect;
import android.os.Handler;
import android.os.Looper;
import android.util.Log;
import android.view.Gravity;
import android.view.View;
import android.view.WindowManager;
import android.view.accessibility.AccessibilityEvent;
import android.view.accessibility.AccessibilityNodeInfo;
import android.view.accessibility.AccessibilityWindowInfo;
import android.widget.TextView;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * B3 redaction: covers on-screen one-time codes with an overlay.
 *
 * A screen-reading agent (screenshot channel) therefore sees
 * "SecretHandle: protected" where the code used to be. The overlay is
 * FLAG_NOT_TOUCHABLE, so the user can still tap the underlying view; only the
 * pixels are covered.
 *
 * Overlays are updated incrementally (add new regions, drop vanished ones) and
 * a 500 ms refresh re-scans the windows, so a mask survives when the last
 * accessibility event came from an unrelated window.
 *
 * Limitation (recorded in the run notes): the accessibility tree still exports
 * the underlying text to any agent that reads it directly; the prototype covers
 * the screenshot channel and the notification channel, which is what the
 * AndroidWorld runner uses. A system_server implementation would redact the
 * node text itself.
 */
public class RedactionAccessibilityService extends AccessibilityService {

    private static final String TAG = "SHRedact";
    private static final Pattern LOOKS_LIKE_SECRET =
            Pattern.compile("(\\bSH-[A-Z0-9]{6,10}\\b)|(\\b\\d{6,8}\\b)");
    private static final long SCAN_INTERVAL_MS = 200;

    private WindowManager wm;
    private final Map<String, View> overlays = new HashMap<String, View>();
    private final Handler handler = new Handler(Looper.getMainLooper());
    private long lastScan;

    private final Runnable refresh = new Runnable() {
        @Override
        public void run() {
            scan();
            handler.postDelayed(this, SCAN_INTERVAL_MS);
        }
    };

    @Override
    protected void onServiceConnected() {
        super.onServiceConnected();
        wm = (WindowManager) getSystemService(WINDOW_SERVICE);
        SecretBrokerService.audit("a11y_connected", "-", "-");
        handler.post(refresh);
        Log.i(TAG, "connected");
    }

    @Override
    public void onAccessibilityEvent(AccessibilityEvent event) {
        if (event == null || wm == null) {
            return;
        }
        if (getPackageName().equals(String.valueOf(event.getPackageName()))) {
            return;
        }
        scan();
    }

    private void scan() {
        if (wm == null) {
            return;
        }
        lastScan = System.currentTimeMillis();
        Set<String> found = new HashSet<String>();
        try {
            List<AccessibilityWindowInfo> windows = getWindows();
            if (windows != null && !windows.isEmpty()) {
                for (AccessibilityWindowInfo w : windows) {
                    AccessibilityNodeInfo root = w.getRoot();
                    // Our own reveal window is the trusted path (FLAG_SECURE);
                    // masking it would hide the code from the user too.
                    if (root != null && getPackageName().contentEquals(root.getPackageName())) {
                        continue;
                    }
                    collect(root, found, 0);
                }
            } else {
                AccessibilityNodeInfo root = getRootInActiveWindow();
                if (root != null && !getPackageName().contentEquals(root.getPackageName())) {
                    collect(root, found, 0);
                }
            }
        } catch (Throwable t) {
            Log.e(TAG, "scan", t);
            return;
        }

        // Drop masks whose region is gone.
        Iterator<Map.Entry<String, View>> it = overlays.entrySet().iterator();
        while (it.hasNext()) {
            Map.Entry<String, View> e = it.next();
            if (!found.contains(e.getKey())) {
                try {
                    wm.removeView(e.getValue());
                } catch (Throwable ignored) {
                    // already detached
                }
                it.remove();
            }
        }
        // Add masks for new regions.
        int added = 0;
        for (String spec : found) {
            if (!overlays.containsKey(spec)) {
                if (addMask(spec)) {
                    added++;
                }
            }
        }
        if (added > 0) {
            SecretBrokerService.audit("mask", "-", "added=" + added + " active=" + overlays.size());
        }
    }

    private void collect(AccessibilityNodeInfo node, Set<String> out, int depth) {
        if (node == null || depth > 40) {
            return;
        }
        CharSequence text = node.getText();
        CharSequence desc = node.getContentDescription();
        String all = (text == null ? "" : text.toString())
                + " " + (desc == null ? "" : desc.toString());
        boolean sensitive = Vault.containsSecret(all);
        if (!sensitive) {
            // The minted handle is public by design: it is what the broker shows
            // instead of the code, so masking it would hide the handle from the
            // user without protecting anything.
            Matcher m = LOOKS_LIKE_SECRET.matcher(all);
            while (m.find()) {
                if (!Vault.isHandle(m.group())) {
                    sensitive = true;
                    break;
                }
            }
        }
        if (sensitive) {
            Rect r = new Rect();
            node.getBoundsInScreen(r);
            if (r.width() > 0 && r.height() > 0) {
                out.add(r.left + "," + r.top + "," + r.right + "," + r.bottom);
            }
        }
        for (int i = 0; i < node.getChildCount(); i++) {
            collect(node.getChild(i), out, depth + 1);
        }
    }

    private boolean addMask(String spec) {
        String[] p = spec.split(",");
        Rect r = new Rect(Integer.parseInt(p[0]), Integer.parseInt(p[1]),
                Integer.parseInt(p[2]), Integer.parseInt(p[3]));
        TextView v = new TextView(this);
        v.setText("SecretHandle: protected");
        v.setTextColor(0xFFE8F0FE);
        v.setTextSize(11);
        v.setGravity(Gravity.CENTER);
        v.setBackgroundColor(0xFF191C24);
        WindowManager.LayoutParams lp = new WindowManager.LayoutParams(
                r.width(), r.height(),
                WindowManager.LayoutParams.TYPE_ACCESSIBILITY_OVERLAY,
                WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE
                        | WindowManager.LayoutParams.FLAG_NOT_TOUCHABLE
                        | WindowManager.LayoutParams.FLAG_LAYOUT_IN_SCREEN
                        | WindowManager.LayoutParams.FLAG_LAYOUT_NO_LIMITS,
                PixelFormat.TRANSLUCENT);
        lp.gravity = Gravity.TOP | Gravity.LEFT;
        lp.x = r.left;
        lp.y = r.top;
        try {
            wm.addView(v, lp);
            overlays.put(spec, v);
            return true;
        } catch (Throwable t) {
            Log.e(TAG, "addView", t);
            return false;
        }
    }

    private void clearOverlays() {
        for (View v : overlays.values()) {
            try {
                wm.removeView(v);
            } catch (Throwable ignored) {
                // already detached
            }
        }
        overlays.clear();
    }

    @Override
    public void onInterrupt() {
        clearOverlays();
    }

    @Override
    public void onDestroy() {
        handler.removeCallbacks(refresh);
        clearOverlays();
        super.onDestroy();
    }
}
