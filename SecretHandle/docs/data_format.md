# Data and result formats

No real dataset is downloaded by this repository.

## Manually provisioned EC2 layout

```text
<data.root>/
├── manifest.json
├── tasks.jsonl
├── trials/
│   └── <trial-id>/
│       ├── task.json
│       ├── agent_artifacts.jsonl
│       ├── delivery_events.jsonl
│       ├── audit_events.jsonl
│       └── outcome.json
├── apps/
│   └── manifest.json
├── devices/
│   └── manifest.json
└── benchmarks/
    ├── androidworld/
    └── spabench/
```

## Required task fields

`task_id`, `seed`, `application`, `secret_type`, `source_class`, `authorized_packages`, destination origin/field/node requirements, lifecycle policy, attack family, condition B0-B3, device ID, agent ID, model ID, and benign/adversarial pair ID.

## Agent artifacts

Each JSONL row requires `trial_id`, `channel`, `timestamp_monotonic`, and either a protected content reference or test-only synthetic content. Channels include model request/response, planner memory, screenshot, accessibility tree/event, action arguments, clipboard, IME, logs, and attacker traffic. Production values must never be collected; only isolated synthetic canaries are permitted.

## Delivery events

Required fields: `trial_id`, package UID, package name, authenticated origin assertion or null, node/window generation, field class, reservation nonce pseudonym, `bytes_crossed`, `application_accepted`, and monotonic timestamp.

## Outcome file

Required fields map directly to `TrialOutcome`: applicability, `E/R/U/L/F/Y` indicators where defined, latency components, policy/false rejection, confirmation count, identity availability, exclusion category, crash recovery outcome, and provenance hashes.

## Splits and pairing

This paper does not define train/calibration splits. Runs are paired by seed and benign/adversarial task variant and blocked by device, agent, model, application, and secret type. Preserve the pair ID and never infer missing pairs silently.

## External benchmark requirements

- **AndroidWorld:** manually clone/install a pinned revision, record commit and task IDs, and expose success plus failure category through `BenchmarkAdapter`.
- **SPA-Bench:** manually provision under the license/registration terms, record version and task IDs, and implement its adapter without changing labels.
- **Open authentication apps:** build from pinned source and record APK hashes and server-oracle schema.
- **Agent runners:** manually clone pinned AppAgent/Mobile-Agent/other repositories and record prompt/model/config hashes.

Unavailable, private, licensed, or authentication-gated data must remain absent and be recorded as an implementation gap, never replaced by an unrelated dataset.
