# Paper implementation specification

Source: `../main.pdf` (53 pages), inspected 2026-10-03.

## Identity and central task

- **Title:** *SecretHandle: OS-Minted, Destination- and Task-Bound Opaque Secrets for Android Mobile AI Agents*.
- **Method:** SecretHandle.
- **Central task:** let an untrusted mobile AI agent use OTPs, credentials, identifiers, clipboard values, or payment tokens without observing the raw value, while the trusted OS constrains resolution to an authenticated task and destination and redacts subsequent observations.
- **Implementation boundary:** this repository provides a runnable reference model, policy/lifecycle engine, synthetic evaluation harness, metrics, plots, and typed adapters. The paper's production mechanism requires AOSP, Android framework, device, agent, and app changes; those hooks are adapter stubs, not simulated as if they were real Android enforcement.

## Algorithms

1. **Algorithm 1, Mint (PDF p.26):** authenticate source, verify task token, intersect task/source/type destinations, derive lifecycle, sample identifier, construct metadata, authenticate canonical encoding, atomically store the secret record, suppress the source-side value, and return an opaque handle.
2. **Algorithm 2, ENTER/Resolve (PDF p.27):** verify task, load and authenticate the record, resolve a fresh trusted target context, test eligibility, reserve atomically (decrementing the remaining use budget at reservation per decision D4), obtain confirmation, revalidate target, register redaction before delivery, inject through a private adapter, then settle the terminal state (consume conservatively on uncertainty) without mutating the authenticated metadata.
3. **Algorithm 3, Observation Redactor (PDF p.28):** for each active obligation visible to an agent principal, resolve stable identity/bounds and mask accessibility/pixel/action/debug fields; fail closed by masking the containing window or suppressing a frame.
4. **Lifecycle/recovery rules (pp.18-20, 24, 28-29, 41-42):** atomic live-to-reserved transition, single-use linearizability, monotonic expiry, revocation, conservative handling of uncertain delivery, and safe rollback only when non-delivery is proven.
5. **Policy attenuation/intersection (pp.17, 25, 27):** destination predicates are conjunctive over package, origin, field, and node; missing mandatory identity fails closed; intersection may narrow but never widen authority.

## Equations and formal objects

- **Eq. (1):** store record `Omega[n] = (s, H, a, z, r)`. The authenticated metadata `H` is immutable so `a = F_K(enc(H))` stays valid for the handle's whole lifetime; the running use budget is separate mutable record state (`remaining_uses`) decremented at reservation per decision D4, never inside `H`.
- **Eq. (2):** `Mint(s, q, sigma, d, tau, c, ti, te, u; Omega)`.
- **Eq. (3):** `Resolve(h, x, tau', t, gamma; Omega)`.
- **Eq. (4):** `Redact(O, R)`.
- **Eq. (5):** agent-view distinguishing advantage. This is documented and supported by trace-pair diagnostics; computational indistinguishability is not empirically proved by code.
- **Eq. (6):** forgery bound `Adv <= Adv_EUF + Q / 2^lambda`; implemented as a numerical upper-bound utility, not as a cryptographic proof.
- **Eq. (7):** typed destination conjunction over package, origin, field, and node.
- **Eq. (8):** exact exposure rate over instrumented artifacts.

## Data structures

- Secret type, lifecycle state, confirmation policy/evidence, provenance, task token, destination predicate, trusted target context, handle metadata, opaque handle, secret record, reservation nonce, injection result, redaction obligation, observation, audit event, trial record, and experiment result.
- Secrets are accepted as bytes and never emitted through public serialization or audit objects.

## Inputs and outputs

- **Mint input:** protected bytes, type, provenance, authenticated task token, source destination evidence, and policy hints. **Output:** opaque handle or typed rejection.
- **Resolve input:** opaque handle, authenticated task token, short-lived target token, monotonic time, confirmation provider, target-context resolver, private injector, and redactor. **Output:** value-oblivious status and audit event; never the secret.
- **Redact input:** structured observation plus active obligations. **Output:** principal-specific masked observation.
- **Experiment input:** YAML config and either synthetic trials or manually provisioned adapter data. **Output:** raw JSONL trials, aggregate JSON/CSV, provenance metadata, and plots generated from those files.

## Metrics

- Exact/normalized exposure `E`; redirection success `R`; legitimate utility `U`; post-entry leakage `L`; forgery acceptance `F`; replay acceptance `Y`.
- Policy rejection, false rejection, confirmation count, crash recovery, identity availability, latency component summaries, memory/CPU/energy fields when supplied, and general-task regression.
- Wilson intervals for binary rates; bootstrap intervals for latency; paired McNemar exact test and paired permutation utility for configured comparisons.

## Baselines and ablations

- **B0 unprotected:** implemented only with synthetic canaries and isolated in-memory destinations.
- **B1 detected placeholder:** deterministic detector/placeholder reference baseline; it deliberately lacks destination binding.
- **B2 platform flow:** adapter contract for Android Autofill/OTP Autofill/Credential Manager; unavailable workflows are `not_applicable`.
- **B3 SecretHandle:** runnable reference model.
- Ablations: no source minting, destination binding, task binding, atomic lifecycle, redaction, origin predicate, or confirmation. Unsafe variants are synthetic-only.

## Data and simulation settings

- Synthetic OTP, credential, identifier, and payment records; correct/wrong package, origin, field, node generation; live/expired/replayed/concurrent cases; modeled accessibility, screenshot, action, clipboard, IME, log, and endpoint artifacts.
- Real targets named by the paper: Pixel userdebug AOSP, limited Samsung/system integration, open authentication apps, AndroidWorld, SPA-Bench, AppAgent, Mobile-Agent family, and a maintained AndroidWorld-compatible agent. No dataset, model, repository, or device image is downloaded here.

## Experimental protocol

- Conditions B0-B3, paired task seeds, device/agent/model/app/secret blocks, seven attack/stress families, protected delivery and artifact oracles, confidence intervals, explicit exclusions, and result provenance.
- The killer experiment requires absence from instrumented artifacts, denial at an attacker destination, and successful legitimate login.

## Assumptions

1. Intact reference monitor and complete mediation.
2. Authentic source and task tokens.
3. Secure HMAC, secret key, random identifiers, canonical injective encoding.
4. Trusted target context equals the actual target at commit.
5. Complete modeled-channel redaction before delivery.
6. Value-oblivious public behavior for equal allowed leakage.

## Limitations and conceptual-only components

- No AOSP implementation, real device measurement, private input dispatcher, screenshot compositor hook, WebView origin attestation, StrongBox guarantee, Protected Confirmation integration, real agent runner, app suite, or benchmark data is present.
- Theorems are conditional specifications, not executable proofs of Android behavior.
- Conceptual trend coordinates in Figure 6 are not implemented as results.
- Parameter values in Table D.6 and compatibility statuses in Table F.8 are intentionally unset.
- Real latency, memory, CPU, energy, user burden, task success, and attack rates require manually provisioned EC2/device infrastructure.

## Placeholder policy

All repository-generated outputs are labeled **synthetic smoke-test output, not a paper result**. Paper placeholders are never copied into result files.
