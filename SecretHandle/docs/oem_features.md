# OEM Features: Missing or Unsupported

This document records OEM-specific capabilities that are absent or unsupported in the research prototype. It is intended to set expectations for reproduction across devices and to flag integration points for OEM support.

## Unsupported OEM features

| Feature | Status | Notes |
|---|---|---|
| StrongBox attestation paths | Partial/unsupported | Keystore attestation is modeled at the API level; hardware-bound attestation via StrongBox varies by OEM/device and is not exercised in the synthetic pipeline. |
| Protected Confirmation UI integration | Unsupported (research only) | Android's Protected Confirmation requires OEM/secure display support; the prototype uses a software oracle and does not claim hardware-protected confirmation. |
| OEM wallet/payment provider extensions | Unsupported | Production wallet extensions (e.g. OEM Pay) are out of scope; research uses synthetic wallet tokens only. |
| OEM-specific accessibility/input patches | Unsupported | Vendor overlays (accessibility, input dispatch) may interfere; the prototype targets AOSP-compatible behavior and records compatibility as N/A when unavailable. |
| Device-specific keymaster implementations | Partial | Keymaster versions differ across SoCs/OEMs; the implementation abstracts via `android.security.keystore` and does not hard-code vendor quirks. |

## Device/emulator test tiers

- Emulator (AOSP image, x86_64): used for B0/B1 smoke and compatibility checks where possible; hardware-backed features may be emulated or absent.
- Cuttlefish: recommended for closer-to-device behavior when AOSP is self-built; StrongBox/attestation behavior may differ from retail devices.
- Physical retail device: final validation tier; requires approval and may have OEM restrictions; not required for the Emerging Ideas evidence.
- Research prototype (synthetic): primary evidence tier (offline, reproducible) — all numbers labeled as synthetic/simulation-only.

## Integration checklist for OEM adoption

1. Map OEM keymaster/StrongBox capabilities to the attestation policy and record support level.
2. Confirm Protected Confirmation availability and fallback policy (fail-closed).
3. Verify accessibility tree stability across OEM skins and Compose/CUSTOM views.
4. Document SELinux policies and any required system permissions for the privileged service.
5. Validate redaction on OEM notification/overlay surfaces.

All "TODO" entries in compatibility tables reflect these gaps; they must be filled with measured values or explicitly marked `unsupported`/`N/A` before submission (see checklist item K4).
