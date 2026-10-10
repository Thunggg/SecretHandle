# Notation consistency check

- `s`: raw secret only.
- `q`: secret type only.
- `sigma`: source/provenance only.
- `tau`: task identity only.
- `d`: destination predicate only.
- `n`: random handle identifier only.
- `H`: full authenticated metadata record only.
- `h`: compact agent-visible handle only.
- `a`: authenticator only.
- `x=(p,o,f,v)`: trusted target context only.
- `p`, `o`, `f`, `v`: package, origin, field class, node token respectively.
- `u`: remaining successful-use budget only.
- `c`: confirmation policy only.
- `z`: lifecycle state only.
- `r`: reservation nonce only.
- `Omega`: trusted record store only.
- `R`: redaction registry only.
- `ell`: explicitly allowed leakage only.
- `E,R,U,L,F,Y` in the experiment section: exposure, redirection, utility, post-entry leakage, forgery acceptance, and replay acceptance. The experimental `R` appears only as a scalar metric; the redaction registry is used in formal/algorithm contexts, so the contexts do not conflict, but a final camera-ready revision may rename the metric to `ASR_redir` for maximal clarity.

Equation labels and theorem labels are unique. Variables in theorem statements match the system model. No undefined constant appears in the final bounds. The only asymptotic parameter is `lambda`; online attempts `Q` is explicit.

Status: **pass with one cosmetic renaming opportunity for experimental R.**
