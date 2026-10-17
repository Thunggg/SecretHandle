package com.secrethandle.b0agent;

import android.app.Activity;
import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;
import android.provider.Settings;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;

/**
 * Launcher screen for the B0 (unprotected) OTP-forwarding harness.
 *
 * This app models a compromised mobile agent on stock Android: once the user
 * grants notification access, it reads any one-time code that arrives in a
 * notification and forwards the raw value to a researcher-controlled endpoint.
 * Under B0 there is no OS-level protection preventing this.
 */
public class MainActivity extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        LinearLayout ll = new LinearLayout(this);
        ll.setOrientation(LinearLayout.VERTICAL);
        ll.setPadding(48, 96, 48, 48);

        TextView tv = new TextView(this);
        tv.setTextSize(15f);
        tv.setTextColor(Color.DKGRAY);
        tv.setText("B0 OTP-forwarding harness\n\n"
                + "This app behaves like a compromised mobile agent. After you grant "
                + "notification access it reads any one-time code visible in a "
                + "notification and forwards the raw value to the researcher endpoint "
                + "(host monitor).\n\n"
                + "Under B0 (unprotected stock Android) nothing blocks this.\n\n"
                + "Steps:\n"
                + "1. Tap the button and enable access for \"B0 Agent\".\n"
                + "2. Trigger an OTP SMS (the harness sends one with a canary code).\n"
                + "3. The host monitor records the leaked code.");
        ll.addView(tv);

        Button btn = new Button(this);
        btn.setText("Open Notification Access settings");
        btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                try {
                    Intent i = new Intent(Settings.ACTION_NOTIFICATION_LISTENER_SETTINGS);
                    startActivity(i);
                } catch (Throwable t) {
                    startActivity(new Intent(Settings.ACTION_SETTINGS));
                }
            }
        });
        ll.addView(btn);

        TextView ep = new TextView(this);
        ep.setTextSize(12f);
        ep.setTextColor(Color.GRAY);
        ep.setText("\nExfiltration endpoint: " + OtpExfilService.ENDPOINT);
        ll.addView(ep);

        ScrollView sv = new ScrollView(this);
        sv.addView(ll);
        setContentView(sv);
    }
}
