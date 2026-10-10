# Mathematical audit

## Result inventory

| Result | Assumptions | Proof status | External theorem | Gap/risk | Dimensions/constants | Strength decision |
|---|---|---|---|---|---|---|
| Lemma 1: Mint-view independence | source/task authenticity; authenticator security/freshness; value-oblivious public behavior; TCB hides store | Complete in model; appendix expansion | None beyond standard indistinguishability and MAC assumptions | Fails if visible metadata, length, timing, or tag encodes the value | Identifier/tag are lambda bits; advantage dimensionless | Kept as conditional lemma |
| Lemma 2: Resolve authorization invariant | reference-monitor integrity; authentic target identity | Complete in transition model | None | Implementation must make the stated guard the only live-to-reserved path | Target components are typed; use count dimensionless | Kept |
| Theorem 1: Destination confinement | Lemma 2; complete mediation; fresh target revalidation; one-shot injection binding | Complete in model | None | WebView origin theorem does not apply without authenticated node-to-origin binding | Predicate output Boolean | Kept; explicitly scoped |
| Theorem 2: Handle unforgeability | EUF-CMA authenticator; canonical encoding; random IDs; secret key | Complete reduction sketch with appendix detail | HMAC security is assumed, not reproved; RFC 2104 cited | Bound must change if tag is truncated or identifiers are predictable | Bound is `Adv_EUF + Q/2^lambda`; all terms dimensionless | Kept; not called tight/optimal |
| Proposition: Single-use linearizability | atomic live-to-reserved CAS; no rollback after possible delivery | Complete invariant proof | Linearizability concept used informally, no external theorem needed | Durable ordering across input delivery and journal is an implementation obligation | Count invariant is dimensionless | Kept |
| Proposition: Expiry monotonicity | monotonic clock; no expired-to-live transition | Complete | None | Suspend/reboot mapping to the clock must be specified | All times same unit | Kept |
| Theorem 3: Agent-view non-disclosure | all six assumptions, especially complete modeled-channel redaction and value-oblivious behavior | Complete in the declared model; not a platform proof | Standard hybrid argument | Omitted channel or value-dependent app behavior invalidates premise; task outcome is declassified | Distinguishing advantage dimensionless | Kept with strong limitations |
| Corollary: Redirection resistance | destination confinement; attacker destination outside predicate | Complete | None | Does not cover same-destination semantic misuse | Boolean match predicate | Kept and narrowed |
| Proposition: Safe attenuation | destination subset; no later expiry; no larger use budget; at-least-as-strict confirmation | Complete set-inclusion argument | None | Requires policy-order definition in code | Use budget integer; time same unit | Kept |

## External-result audit

- HMAC is used as an example implementation and cited to RFC 2104; the manuscript assumes EUF-CMA security rather than claiming RFC 2104 itself proves the full implementation.
- OAuth resource indicators, DPoP, and WebAuthn are design analogies; none is invoked as a theorem about Android UI targets.
- No classical impossibility or optimization theorem is invoked.
- No missing “Idea 3” or “Idea 8” result is used. The task-token contract is specified independently.

## Dimensional consistency

- `t_i`, `t_e`, and resolver time `t` must use the same monotonic-clock unit.
- `u`, event counts, and attempts `Q` are dimensionless nonnegative integers.
- `lambda` is a bit-length/security parameter.
- Advantages and probabilities are dimensionless and in `[0,1]`.
- Destination components package/origin/field/node are distinct types; the policy does not compare unlike identities.

## Required implementation validation

The formal results become applicable to a prototype only after tests establish complete mediation, target-token freshness, atomic reservation/delivery ordering, redaction coverage, canonical encoding, key security level, uniform error behavior, and absence of raw-value logging. These are listed as theorem assumptions, not silently inferred.
