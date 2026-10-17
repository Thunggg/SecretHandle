# Implementation gaps

## Blocking gaps for paper-level experiments

| Gap | Why Python cannot supply it | Required external work | Status |
|---|---|---|---|
| AOSP system service and binder authorization | Requires Android framework source/build/signing | Implement service in `system_server`, allowlisted source calls, task-token verification, audit export | adapter stub |
| Durable secret store and crash journal | Python lock is not Android durable state | Encrypted/locked storage, fsync ordering, rollback protection, multi-user separation, recovery tests | adapter stub |
| Hardware-backed key evidence | Host HMAC does not establish TEE/StrongBox | Android Keystore key generation, attestation/security-level reporting, backup/restore review | adapter stub |
| Authoritative source adapters | SMS/Credential Manager/clipboard/wallet pipelines are Android-specific | Implement and document provenance contracts; never handle production secrets in experiments | adapter stub |
| Authenticated task token | Reference token is a typed object | OS signature/ownership format, anti-replay, allowed-app intersection, task lifecycle | adapter stub |
| Target node token | In-memory token does not bind a live UI node | Window/connection/node/generation/UID binding, short TTL, refetch at commit | adapter stub |
| WebView origin attestation | Package identity cannot authenticate frame origin | Browser/WebView changes for node-to-frame-to-origin binding; fail closed otherwise | unresolved research gap |
| Private input path | In-memory injector does not bypass agent/IME | Framework input capability bound to reservation and target generation | adapter stub |
| Pixel/accessibility redaction | Structured strings do not prove buffer-level coverage | Principal-specific screenshot composition and accessibility/event serialization before agent mapping | adapter stub |
| Protected Confirmation | Synthetic provider is not trusted UI | Bind reservation/task/destination/transaction digest to platform confirmation | adapter stub |
| Real apps and endpoints | Not present and must be isolated | Build open test apps and protected verifier/attacker endpoints; record hashes | manual provisioning |
| Agents/models | External repositories/models are absent | Pin AppAgent/Mobile-Agent/other runner and cloud/local model versions | manual provisioning |
| AndroidWorld/SPA-Bench | External licensed/versioned files absent | Manually provision and implement schema-preserving adapters | manual provisioning |
| Device metrics | CPU/energy/memory/latency need device instrumentation | Perfetto/Batterystats/power tooling and synchronized component traces | manual provisioning |
| Detector baseline equivalence | External implementation/API not specified in the paper | Obtain exact repository or document a scoped reimplementation after author review | author verification |

## Non-blocking reference-model limits

- Python cannot reliably wipe immutable byte copies or lock memory.
- Synthetic HMAC keys derived from seeds are test-only and intentionally insecure for production.
- Deterministic latency values test analysis plumbing; they are not performance data.
- The disclosure oracle covers exact, base64, URL, JSON, Unicode-normalized, numeric-normalized, and space/dash-separated digit forms. OCR and image-content scanning require an external adapter.
- The adapter interfaces are frozen at contract v1 (2026-10-17); external implementations must satisfy `tests/test_adapter_contracts.py`.
- The authenticated metadata `H` is immutable; the remaining use budget is tracked as mutable record state and decremented at reservation (decision D4), so `a = F_K(enc(H))` stays valid for the handle's whole lifetime.
- The reference redactor masks items associated with a registered target token; propagation to application-created echo views remains an AOSP taint/obligation problem.
- Exact computational non-disclosure, complete-channel closure, and EUF-CMA security are assumptions/theorems, not pytest outcomes.

No unavailable component is silently replaced by a real-result claim.
