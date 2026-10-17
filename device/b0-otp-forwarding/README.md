# B0 OTP-forwarding harness (Android emulator)

Preliminary, emulator-based reproduction of attack 1 ("read and exfiltrate")
under the **B0 (unprotected)** baseline from the paper.

> Scope note: this is **emulator evidence for functional correctness**, not a
> paper result and not a device-latency measurement. Per Section
> "Prototype configurations", emulator runs do not count as evidence for
> hardware-protected keys or real-device latency. No attempt is made here to
> build B3/SecretHandle on AOSP; this harness only shows that the attack works
> on unprotected stock Android.

## Components

- `android/` — a single APK (`com.secrethandle.b0agent`) modelling a
  compromised mobile agent. `OtpExfilService` is a `NotificationListenerService`
  that reads any one-time code appearing in a notification and POSTs the raw
  value to the host.
- `monitor/monitor.py` — host-side disclosure monitor. Receives exfiltrated
  payloads on `0.0.0.0:8787`, logs them to `monitor/exfil_log.jsonl`, and flags
  any payload containing the run's canary value.
- `monitor/run_rate.py` — drives repeated trials (one fresh canary per trial,
  unique sender so each notification carries only its own code), then reports an
  exposure rate with a Wilson 95% interval to `monitor/rate_results.json`.
- `build.ps1` — Gradle-free CLI build (aapt2 + javac + d8 + zipalign +
  apksigner). Java tools are launched via `Start-Process` because direct
  invocation hangs in some non-interactive shells.

## Build

```powershell
pwsh -File build.ps1     # or: & .\build.ps1
# -> build\b0agent.apk
```

Requires: Android SDK build-tools 35.0.0 and `platforms/android-34/android.jar`;
Android Studio's bundled JBR (`C:\Program Files\Android\Android Studio\jbr`).

## Reproduce (emulator already running)

```powershell
$adb = "$env:LOCALAPPDATA\Android\Sdk\platform-tools\adb.exe"

# 1. install and grant notification access
& $adb install -r -g build\b0agent.apk
& $adb shell settings put secure enabled_notification_listeners `
    "com.secrethandle.b0agent/com.secrethandle.b0agent.OtpExfilService"

# 2. make Google Messages the default SMS app
& $adb shell settings put secure sms_default_application com.google.android.apps.messaging
& $adb shell pm grant com.google.android.apps.messaging android.permission.POST_NOTIFICATIONS

# 3. start the host monitor with the run's canary
.venv\Scripts\python.exe monitor\monitor.py 482913

# 4. trigger an OTP SMS and watch the monitor
& $adb emu sms send 15551234567 "Your SecretHandle verification code is 482913. Do not share it."
```

## Observed result (2026-10-17, emulator-5554, Android 14 / SDK 34)

On stock Android the notification listener read the code and forwarded it:

```
# app logcat
B0Agent : posted from com.google.android.apps.messaging: (555) 123-4567 Your SecretHandle verification code is 482913. Do not share it.
B0Agent : forwarded otp=482913 -> HTTP 200

# monitor/exfil_log.jsonl
{"time":"2026-10-17T08:46:12.737822+00:00","path":"/exfil","canary":"482913","canary_match":true,
 "payload":{"source":"com.google.android.apps.messaging","otp":"482913","context":"... verification code is 482913 ..."}}
```

`canary_match: true` = the raw canary secret reached the attacker-controlled
endpoint. This is the B0 vulnerability reproduced end to end.

## Rate run (metric E, emulator only)

`python monitor/run_rate.py 10 2.5` sends 10 canaries from 10 distinct senders
and checks each against what reached the monitor:

```
trials  leaked  exposure_rate  wilson_low  wilson_high
  10      10        1.0           0.722        1.0
```

All 10 trials leaked (`received_count: 10`). On unprotected stock Android the
notification listener is not restricted in any way, so exposure is deterministic.
This is a **functional reproduction rate on an emulator**, not a paper number.

## Caveats / next steps

- Rate is `n=10` on one emulator image; increase `n` and vary the Android
  version for a defensible figure. Still not a substitute for real-device runs.
- Emulator only: no hardware keystore, no real-device latency/energy claims.
- Demonstrates B0 only. The B3 (SecretHandle) countermeasure requires the AOSP
  `system_server` implementation (Plan B / Track A) and is out of scope here.
