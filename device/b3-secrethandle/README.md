# B3 SecretHandle prototype (stock Android, emulator)

Countermeasure module for the **B3 (SecretHandle)** condition in the paper.
It runs on unmodified Android 13 (API 33) as a privileged-by-grant app and
demonstrates the two mechanisms that the `system_server` design would implement
natively:

1. **Mint / redact at the notification channel.** A `NotificationListenerService`
   detects a one-time code in a posted notification, mints an opaque handle
   (`SH-XXXXXX`), cancels the original notification and posts a redacted
   replacement that contains only the handle.
2. **Redact on screen.** An `AccessibilityService` scans the foreground window
   for the protected plaintext and covers the matching node bounds with a
   `TYPE_ACCESSIBILITY_OVERLAY` view (`SecretHandle: protected`). The overlay is
   `FLAG_NOT_TOUCHABLE`, so taps still reach the app.

The plaintext lives only in the broker's in-memory `Vault`, bound to a 5-minute
TTL and resolvable **exactly once** through `MainActivity` (the explicit
*resolve* step). Every mint / mask / resolve / deny is appended to
`files/audit.jsonl`.

## Layout

```
android/AndroidManifest.xml                  two services + launcher activity
android/res/xml/accessibility_service_config.xml
android/src/com/secrethandle/b3/Vault.java               handle minting, TTL, one-time
android/src/com/secrethandle/b3/SecretBrokerService.java notification redaction + audit
android/src/com/secrethandle/b3/RedactionAccessibilityService.java overlay redaction
android/src/com/secrethandle/b3/MainActivity.java        status + reveal
build_linux.sh                               aapt2/javac/d8/zipalign/apksigner
```

## Build

```bash
bash build_linux.sh      # -> build/b3secrethandle.apk
```

Needs Android SDK build-tools 35.0.0 and `platforms/android-34/android.jar`
(`ANDROID_HOME` or `~/android-sdk`).

## Install and enable (emulator)

```bash
adb install -r build/b3secrethandle.apk

# notification listener (API 34+ needs the cmd form, settings alone is not enough)
adb shell cmd notification allow_listener \
  com.secrethandle.b3/com.secrethandle.b3.SecretBrokerService

# accessibility service
adb shell settings put secure enabled_accessibility_services \
  com.secrethandle.b3/com.secrethandle.b3.RedactionAccessibilityService
adb shell settings put secure accessibility_enabled 1
```

## Quick check

```bash
# canary SMS; the shade must show "SH-XXXXXX", never the code
adb emu sms send +15551230001 "SecretHandle test: your verification code is SH-95F9E6. Do not share it."
adb shell dumpsys notification --noredact | grep -i secrethandle

# open the SMS app and screenshot: the message must be covered by the overlay
adb exec-out screencap -p > /tmp/b3.png

# audit trail
adb shell run-as com.secrethandle.b3 cat files/audit.jsonl
```

Expected: the original notification is cancelled and replaced by
`SH-XXXXXX ... from <pkg>`; the SMS conversation shows the mask; the reveal
button returns the code once, then reports "expired or already used".

## Fidelity and limitations (state these in the paper)

- **Not `system_server`.** The broker is an ordinary app holding two grant-based
  capabilities. It shows that the *policy* (mint, redact, TTL, one-time resolve,
  audit) is implementable and measurable, not that it is enforced by the OS.
  The deployment path is the `system_server` patch in `aosp-patches/`
  (notification interception in `NotificationManagerService` + node-text
  redaction in `AccessibilityManagerService`/`WindowManagerService`).
- **Accessibility tree is not redacted.** The overlay hides pixels (screenshot
  channel), but the underlying `AccessibilityNodeInfo` text is still exported to
  agents that read the tree directly. The AndroidWorld runner used for the
  B0/B3 comparison consumes screenshots, so the measured leak rate is valid for
  that threat model; a tree-reading agent is out of scope for this prototype.
- **Heuristic detection.** Codes are found with a numeric/alphanumeric regex.
  A production design would use the notification's template/category and the
  sender identity instead.
- Emulator only: no hardware keystore, no real-device latency or energy claim.
