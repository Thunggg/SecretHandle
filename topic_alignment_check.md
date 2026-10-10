# Topic alignment check

Audit date: 2026-10-03.

The manuscript was compared against the locked canonical specification in `idea_fidelity_report.md` and the machine-readable `topic_signature.json`.

| Locked object | Manuscript realization | Result |
|---|---|---|
| Android/mobile-agent security topic | Title, abstract, introduction, model, design, and evaluation all center Android GUI-operating agents. | Pass |
| SecretHandle mechanism | The system is consistently named SecretHandle and uses OS-minted opaque handles. | Pass |
| Authoritative-source minting | SMS/notification, Credential Manager, clipboard/profile, and wallet adapters mint before agent observation. | Pass |
| Destination and task binding | The record contains destination predicate `d` and task identity `tau`; resolution authenticates the live target context. | Pass |
| `ENTER(handle)` action | Represented as `ENTER(handleId, targetNodeToken)` and formalized through the resolve transition. | Pass |
| Typed lifecycle | TTL, use budget, reservation, consumption, revocation, confirmation, and crash recovery are explicit. | Pass |
| Observation redaction | Accessibility events/trees and screenshot pixels are masked before and after private injection. | Pass |
| Formal goals | Conditional non-disclosure, destination confinement, unforgeability, single-use, expiry, and attenuation results are stated and proved. | Pass |
| Experiment family | AOSP devices, open apps, agents, redirection/forgery/replay/reread attacks, baselines, metrics, and ablations are specified. | Pass |
| Evidence honesty | No implementation or measurement is claimed; tables and curves are labeled planned/placeholder. | Pass |
| Excluded topics | Federated learning, blockchains, mechanism design, and generic alignment do not appear as contributions. | Pass |

Terminology check: title/abstract/introduction contain SecretHandle, OS-minted, destination-bound, opaque handles/secrets, mobile AI agents, Android, authoritative source, `ENTER(handle)`, lifecycle, and observation redaction.

Result: **no topic drift detected.** The one intentional title refinement adds “task-bound,” which is part of the canonical record and sharpens rather than changes the idea.
