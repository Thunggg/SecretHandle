# Implementation notes

The paper specifies an Android reference monitor but intentionally reports no implementation. This repository therefore separates two layers:

1. A complete executable **reference semantics** for records, policies, HMAC authentication, mint, resolve, lifecycle, redaction obligations, audit projections, metrics, and synthetic trials.
2. Explicit **external adapters** for actions that only Android/device/agent infrastructure can perform.

## Translation choices

- Paper tuple `Omega[n]` becomes `SecretRecord` behind `SecretStore`; the raw bytes field is excluded from public results and audit events.
- `H` becomes immutable `HandleMetadata`. Canonical sorted-key JSON is the versioned `enc(H)` used by HMAC-SHA-256.
- Destination policy is a finite conjunction over sets of acceptable package, origin, field, and node values. `None` is an explicit wildcard; missing required target identity is rejection.
- Task tokens contain an authenticated task ID and allowed-package set in the reference model. Real signature/OS ownership verification belongs in an AOSP adapter.
- Confirmation is post-reservation, matching Algorithm 2. The core separates precheck eligibility from confirmation because the prose definition includes confirmation in the combined abstract predicate.
- The target resolver is called twice. Full `TargetContext` equality includes window, generation, node, package, origin, and field.
- A single-use uncertain delivery consumes the record. Rollback requires an adapter to report `NOT_DELIVERED`, modeling a durable proof that bytes did not cross the boundary.
- Redaction obligations identify the target token and type, not the secret. Synthetic observations are structured records; real screenshot/accessibility transformation must implement the same adapter semantics below the agent boundary.
- Synthetic baseline outputs exercise the analysis pipeline. They are deliberately simple and never presented as performance measurements.

## Security posture

This is not a secret-management library for production. Python memory cannot guarantee wiping, locked pages, TEE keys, screenshot composition, or complete mediation. The code is intended to make state transitions, failure semantics, metrics, and external contracts reviewable before AOSP engineering begins.
