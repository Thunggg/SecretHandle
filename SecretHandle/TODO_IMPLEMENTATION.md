# TODO implementation

## AOSP mechanism

- [ ] Pin an AOSP commit/device branch and implement the binder service, permission model, task-token verifier, source allowlist, store, lifecycle journal, quotas, and protected audit export.
- [ ] Implement SMS/notification, research Credential Manager, sensitive clipboard, and research wallet adapters with precise provenance contracts.
- [ ] Implement short-lived target tokens bound to window, connection, node, generation, package UID, origin assertion, and expiry.
- [ ] Implement reservation-bound private input that bypasses agent-visible action arguments and ordinary IME history.
- [ ] Implement principal-specific accessibility tree/event and screenshot-buffer redaction before data reaches the agent.
- [ ] Establish WebView main/nested-frame origin identity or fail closed; obtain author review for any weaker policy.
- [ ] Integrate platform/protected confirmation with a digest of destination, task, transaction context, handle ID, and reservation nonce.
- [ ] Add durable crash tests at every reserve/register/inject/commit boundary and validate no rollback after possible delivery.
- [ ] Review canonical encoding, key separation, tag length, backup/restore, multi-user behavior, and rollback protection with Android security reviewers.

## Applications, agents, and data

- [ ] Build and hash the four open synthetic-secret apps and isolated verifier/attacker services.
- [ ] Manually provision pinned AndroidWorld and SPA-Bench versions on EC2; implement adapters and record license/registration steps.
- [ ] Manually provision pinned AppAgent, Mobile-Agent, and one maintained AndroidWorld-compatible agent plus cloud/local model configurations.
- [ ] Resolve a stable DroidRun version only if it remains an evaluated implementation.
- [ ] Implement protected artifact monitors for model traffic, planner state, accessibility, pixels/OCR, actions, clipboard, IME, logs, crash data, and attacker traffic.

## Baselines and experimental design

- [ ] Verify the exact B1 detector/placeholder implementation or scope the reference baseline explicitly with author approval.
- [ ] Implement B2 Autofill/OTP Autofill/Credential Manager flows for cooperating apps and record unsupported workflows as not applicable.
- [ ] Freeze identifier bits, tag bits, TTL, use budgets, rate limits, observation duration, repetitions, bootstrap count, outlier policy, and primary comparisons before examining outcomes.
- [ ] Add real paired McNemar/permutation analysis and device-blocked reporting after raw trials exist.
- [ ] Replace deterministic synthetic latency with measured component/device traces only in a provenance-marked real run.

## Verification and release

- [ ] Add property-based policy tests and model-based crash/concurrency schedules.
- [ ] Add Android instrumented/unit/end-to-end tests separated from emulator-only tests.
- [ ] Run `ruff` and `mypy` in a provisioned development environment and resolve findings; they were not installed for the initial local audit.
- [ ] Add CI for Python 3.11/3.12 and a separate manually triggered device pipeline.
- [ ] Publish source/build manifests, scripts, schemas, raw secret-free outcomes, licenses, and a one-command isolated canary smoke test.
