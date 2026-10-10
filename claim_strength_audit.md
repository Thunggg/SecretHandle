# Claim-strength audit

| Strong term/claim | Audit | Action |
|---|---|---|
| “first” | Not justified by an exhaustive search | Removed from manuscript. |
| “optimal” | No optimization/lower-bound proof | Not used for SecretHandle. |
| “sharp” | No sharp threshold proof | Not used. |
| “matching” | No matched upper/lower result | Not used. |
| “exact” | Used only for exact canary-string matching, not a universal security claim | Kept in metric definition. |
| “zero exposure/redirection” | No measurements; observed zero would not prove impossibility | Reframed as a target and “0 of n” reporting rule. |
| “proven mechanism” | A killer-experiment success would not prove the whole system | Removed; experiments validate observations, while theorems remain conditional on model assumptions. |
| “unforgeable” | Cryptographic property is conditional on MAC, entropy, canonical encoding, and key secrecy | Kept only in definition/theorem with assumptions. |
| “raw value never enters the agent view” | Only defensible for enumerated modeled channels under complete redaction/source assumptions | Scoped throughout. |
| “defeats prompt injection” | Too broad | Replaced by “rejects resolution at destinations outside the binding even when the agent is steered.” |
| “state of the art” / “superior” | No real comparative results | Not used. |
| “no functionality loss” | Unsupported | Not used; utility is an empirical metric. |
| Novelty statement | Search not exhaustive and closest 2026 work exists | Qualified as “within the verified literature” and bounded to four simultaneous properties. |

Result: all unsupported superlatives were removed or weakened.
