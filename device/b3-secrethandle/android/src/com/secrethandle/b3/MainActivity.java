package com.secrethandle.b3;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.provider.Settings;
import android.view.View;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;

/**
 * Status and the explicit Resolve step.
 *
 * The activity lists the handles currently in the vault. Revealing one is a
 * single-use action and is written to the audit log, which is what the paper
 * calls an accountable resolve.
 */
public class MainActivity extends Activity {

    private LinearLayout list;
    private TextView status;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        // The reveal window is the trusted path: the OS keeps it out of screen
        // capture (screencap, screen record, the emulator gRPC screenshot), so
        // the user can read the code while a screen-reading agent cannot.
        getWindow().setFlags(
                WindowManager.LayoutParams.FLAG_SECURE,
                WindowManager.LayoutParams.FLAG_SECURE);

        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        int pad = (int) (16 * getResources().getDisplayMetrics().density);
        root.setPadding(pad, pad, pad, pad);

        status = new TextView(this);
        status.setTextSize(13);
        status.setText("SecretHandle B3 prototype\n\n"
                + "1. Enable the notification listener\n"
                + "2. Enable the accessibility service\n"
                + "Codes are replaced by handles; the screen is masked.");
        root.addView(status);

        Button notif = new Button(this);
        notif.setText("Notification access settings");
        notif.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(Settings.ACTION_NOTIFICATION_LISTENER_SETTINGS));
            }
        });
        root.addView(notif);

        Button a11y = new Button(this);
        a11y.setText("Accessibility settings");
        a11y.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(Settings.ACTION_ACCESSIBILITY_SETTINGS));
            }
        });
        root.addView(a11y);

        list = new LinearLayout(this);
        list.setOrientation(LinearLayout.VERTICAL);
        ScrollView scroll = new ScrollView(this);
        scroll.addView(list);
        root.addView(scroll, new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT, 0, 1f));

        Button refresh = new Button(this);
        refresh.setText("Refresh");
        refresh.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                render();
            }
        });
        root.addView(refresh);

        setContentView(root);
    }

    @Override
    protected void onResume() {
        super.onResume();
        render();
    }

    private void render() {
        list.removeAllViews();
        final java.util.List<Vault.Entry> entries = Vault.entries();
        if (entries.isEmpty()) {
            TextView empty = new TextView(this);
            empty.setText("No protected codes.");
            list.addView(empty);
            return;
        }
        for (final Vault.Entry e : entries) {
            TextView row = new TextView(this);
            row.setTextSize(13);
            row.setText(e.handle + "  from " + e.source
                    + (e.used ? "  [used]" : ""));
            list.addView(row);
            if (!e.used) {
                Button reveal = new Button(this);
                reveal.setText("Reveal " + e.handle);
                reveal.setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        String secret = Vault.reveal(e.handle);
                        SecretBrokerService.audit(
                                secret == null ? "deny" : "resolve",
                                e.handle, "ui");
                        status.setText(secret == null
                                ? "Handle " + e.handle + " is expired or already used."
                                : "Code for " + e.handle + ": " + secret);
                        render();
                    }
                });
                list.addView(reveal);
            }
        }
    }
}
