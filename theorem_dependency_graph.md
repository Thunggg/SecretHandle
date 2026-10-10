# Theorem dependency graph

```text
A1 Reference-monitor integrity -------------------+
                                                    +--> Lemma 2: authorization invariant
A4 Authentic target identity ---------------------+                 |
                                                                      +--> Theorem: destination confinement
                                                                      |          |
                                                                      |          +--> Corollary: reject redirection outside d
                                                                      +--> Proposition: single-use safety

A2 Source/task authenticity ----+
A3 MAC security + random IDs ----+--> Lemma 1: mint-view independence ----+
A6 Value-oblivious behavior -----+                                       |
                                                                          +--> Theorem: agent-view non-disclosure
A1 Reference-monitor integrity ------------------------------------------+
A5 Complete modeled-channel redaction -----------------------------------+

A3 MAC security + canonical encoding + random IDs --> Theorem: handle unforgeability

Monotonic clock + no expired-to-live transition --> Proposition: expiry monotonicity

Policy subset + shorter lifetime + lower use budget + stronger confirmation
    --> Proposition: safe attenuation

Theorems/propositions
    --> Experiment oracles: exposure, redirection, forgery, replay, reread, latency
```

No experiment is used as a premise of a theorem. Experiments instead test whether the implementation appears to satisfy the assumptions and whether utility/overhead are acceptable.
