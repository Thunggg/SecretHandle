# Reviewer audit

Audit date: 2026-10-03. This review treats the manuscript as a systems-security submission and distinguishes fatal scientific gaps from editorial issues.

## Summary judgment

The draft is a rigorous specification, formal analysis, and preregistered evaluation plan for SecretHandle. It is not yet submission-ready as an empirical systems paper because the AOSP implementation and measurements do not exist. The manuscript is unusually explicit about that boundary and does not fabricate results.

## Strengths

1. **Clear systems abstraction.** Mint-before-observation and authorize-the-sink form a coherent reference-monitor boundary for mobile-agent secrets.
2. **Threat-model precision.** The draft separates an untrusted agent and injected content from an uncompromised Android reference monitor, and explicitly excludes malicious allowed destinations and unmodeled side channels.
3. **Formal/implementation correspondence.** Assumptions map to source authentication, target identity, MAC protection, atomic lifecycle, and redaction obligations rather than floating as purely mathematical premises.
4. **Honest evidence discipline.** The evaluation is a concrete protocol with protected canary and delivery oracles; no placeholder coordinate is described as measured.
5. **Novelty restraint.** The closest 2026 mobile-placeholder work is acknowledged, and priority language is bounded to the verified search rather than asserted exhaustively.
6. **Reproducibility planning.** Devices, app classes, attacks, baselines, metrics, exclusions, confidence intervals, artifacts, and acceptance criteria are specified before data collection.

## Major issues before submission

1. **Implementation is mandatory.** A competitive mobile-systems/security venue will require a working AOSP prototype, patch-level architecture, and evidence that the private injection and redaction paths are implementable on current Android.
2. **Observation completeness must be tested adversarially.** Accessibility trees/events, screenshots, IME state, clipboard, action arguments, logs, crash reports, and network/model traces need independent canary monitors. Any uncovered path narrows the theorem-to-system claim.
3. **Authenticated target identity is the hardest systems problem.** Native views, Compose, custom Canvas controls, WebView main/nested frames, recycled nodes, and package replacement require separate evidence. WebView origin-to-node binding cannot be assumed from package identity.
4. **Crash and concurrency semantics need implementation proof.** Single-use claims require linearizable reservation/commit, conservative recovery, and concurrent replay tests on durable state.
5. **Utility and overhead need real results.** Login, 2FA, address entry, credentials, and checkout should report task success, user intervention, p50/p95 latency, memory, energy, and failure categories across devices and agents.
6. **Literature verification needs one final pass.** Nuanced comparisons now supported only at abstract level should be upgraded to full-text section-level evidence; arXiv records should be replaced by archival versions when available.

## Minor issues

- Select the actual Elsevier journal or change to the target conference class; anonymous author/affiliation metadata remain placeholders.
- Freeze identifier length, authenticator length, TTLs, rate limits, observation duration, run counts, bootstrap repetitions, and outlier policy before experiments.
- Add a compact implementation-diff table after the prototype exists, locating each hook in Android services and data paths.
- Report unsupported UI/source combinations as results rather than excluding them.
- Consider releasing a small mechanized model or property-test harness for the reservation state machine.

## Verdict at current stage

**Strong research blueprint; reject as a completed empirical systems paper until implementation and evaluation are supplied.** The formal claims are appropriately conditional and can remain, provided the final paper reports which assumptions the implementation actually satisfies.
