# SecretHandle reference implementation

This repository translates *SecretHandle: OS-Minted, Destination- and Task-Bound Opaque Secrets for Android Mobile AI Agents* into a runnable Python reference model, synthetic evaluation harness, typed external adapters, metrics, plotting, tests, and paper-to-code audits.

> **Result warning:** No paper-level experimental results are claimed by this repository unless real benchmark outputs are generated and their provenance is recorded.
>
> **Provisioning warning:** This repository does not automatically download datasets or run paper-level experiments. Real experiments are intended to be executed on EC2 after the required datasets, benchmarks, models, and credentials are manually provisioned.

The Python package validates the algorithms and state-machine semantics on synthetic canaries. It is **not** an AOSP security boundary and cannot establish the paper's Android, StrongBox, WebView, screenshot, accessibility, or private-input assumptions.

## Implemented paper objects

- Algorithm 1: authoritative-source `Mint`, typed lifecycle, task/source/type policy intersection, random opaque identifiers, canonical HMAC authentication, and atomic insertion.
- Algorithm 2: `ENTER/Resolve`, target-token lookup, eligibility, atomic reservation, confirmation, target revalidation, pre-delivery redaction, private-injector adapter, conservative finalization, replay prevention, expiry, revocation, and recovery.
- Algorithm 3: structured principal-specific redaction with fail-closed frame suppression.
- Equations (1)-(4), (6)-(8); Equation (5) has a deterministic trace diagnostic but remains a cryptographic definition, not an executable proof.
- Metrics `E`, `R`, `U`, `L`, `F`, `Y`, Wilson intervals, seeded bootstrap intervals, exact McNemar, paired permutation, exclusions, and latency summaries.
- Baselines B0 unprotected, B1 deterministic reference placeholder, B2 external Android platform adapter, and B3 SecretHandle reference model.
- Synthetic attack cases: benign use, cross-destination redirect, fake handle, replay, reread, and expiry.

See [the implementation specification](audits/paper_implementation_spec.md), [traceability matrix](audits/paper_to_code_traceability.csv), and [math audit](audits/math_to_code_audit.md) for exact page/algorithm mappings.

## Installation

Python 3.11+ is recommended for EC2. The local validation environment used Python 3.9 compatibility mode.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'
```

No install is needed for the repository scripts; they add `src/` explicitly.

## Quick start

```bash
python -m secrethandle.cli --help
python scripts/run_synthetic_demo.py --config configs/synthetic_demo.yaml
python scripts/make_plots.py \
  --input outputs/synthetic_demo/metrics.csv \
  --output outputs/synthetic_demo/plots
python scripts/run_experiment.py --config configs/synthetic_demo.yaml --stage killer
```

Every generated local artifact is labeled **synthetic smoke-test output, not a paper result**. Outputs contain trial outcomes and provenance, never canary values.

## Real-data and device usage

Real mode is deliberately non-operational until external components are supplied. Copy `configs/experiment_template.yaml`, set `data.root`, and manually provision:

- a pinned userdebug AOSP build and compatible Pixel device;
- the SecretHandle binder service and framework hooks;
- open login/OTP, 2FA, identifier/checkout, and wallet test apps;
- AndroidWorld and optionally SPA-Bench files;
- pinned AppAgent/Mobile-Agent/other agent repositories and model configurations;
- protected canary/delivery monitors and an isolated attacker endpoint.

Then implement the contracts in `src/secrethandle/adapters.py` and follow [the EC2 guide](docs/ec2_experiment_guide.md). The repository never downloads or launches these dependencies itself.

## Configuration

- `run.seed`: global deterministic seed.
- `security.lambda_bits`: random handle-identifier security parameter; at least 96 and byte-aligned.
- `data.mode`: `synthetic` or `real`; real mode requires `data.root`.
- `experiment.conditions`: B0-B3 identifiers.
- `experiment.attacks`: attack/stress names.
- `experiment.trials_per_attack`: synthetic repetition count or a placeholder to freeze by prospective analysis for real runs.
- `output.dir`: run-specific output directory.

Configs are captured with a SHA-256 digest. Keys whose names resemble secrets, credentials, passwords, tokens, or API keys are redacted from provenance.

## Outputs

The runner generates:

- `trials.jsonl`: secret-free per-trial outcomes;
- `summary.json`: applicability-aware aggregate metrics and Wilson intervals;
- `metrics.csv`: plotting input generated from the summary;
- `provenance.json`: seed, environment, public config, and explicit real/synthetic status;
- `plots/*.png`: charts generated from `metrics.csv`, visibly labeled synthetic.

No paper table or conceptual Figure 6 coordinate is copied into these outputs.

## Tests

```bash
python3 -m pytest -q
```

The suite covers imports, schemas, policy intersection, canonical authentication, lifecycle, expiry, concurrency, resolver decisions, redaction, oracles, metrics, confidence intervals, baselines, config validation, CLI execution, output integrity, and fixed-seed reproducibility. It requires no network, dataset, model, GPU, Android device, or credential.

`ruff` is optional (`python3 -m ruff check .`) and was not available in the initial local environment; no lint pass is claimed unless it is installed and run.

## Repository layout

```text
SecretHandle/
├── audits/          paper mapping, math/result/gap audits
├── configs/         synthetic and EC2 templates
├── docs/            schemas, adapters, implementation, EC2, reproducibility
├── examples/        minimal synthetic config
├── outputs/         generated artifacts only
├── scripts/         demo, experiment, and plotting entry points
├── src/secrethandle reference package
└── tests/           offline pytest suite
```

## Limitations and known gaps

- Python locks model atomicity but do not prove Android database/input durability.
- Structured redaction tests do not prove pixel-buffer or accessibility-framework coverage.
- B1 is a simple fully disclosed reference placeholder, not external authors' source code.
- B2, agent runners, benchmarks, WebView origin attestation, device security level, power measurement, protected confirmation, and OEM hooks are adapter gaps.
- The formal non-disclosure and unforgeability results remain conditional; tests only check controlled examples.
- Synthetic metrics demonstrate pipeline behavior and are not estimates of real attack or task-success rates.

See [implementation gaps](audits/implementation_gaps.md) and [TODO_IMPLEMENTATION.md](TODO_IMPLEMENTATION.md) before any paper-level run.
