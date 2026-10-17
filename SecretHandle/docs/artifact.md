# Artifact Appendix

This document describes the SecretHandle artifact for reproducibility and artifact-evaluation purposes.

## Purpose

The artifact contains:
- Reference model (Python) for reproducing the mathematical guarantees and smoke tests.
- Canary-isolation smoke test (offline) to detect leakage of minted secrets.
- Build scripts, schemas, and configuration files for the synthetic evidence pipeline.
- Documentation of the prototype architecture, evaluation plan, and design decisions.

## Requirements

- Python 3.11 or 3.12
- Virtual environment (recommended)
- Git (to reproduce the commit that produced the submission)
- For device/emulator experiments (optional, hardware-dependent): Android SDK platform-tools, Java 17, and a compatible AVD or physical device. See `docs/reproducibility.md`.

## One-command checks (offline)

From `SecretHandle/`:
```bash
make check
```
This runs: lint (`ruff check`), typecheck (`mypy`), unit tests (`pytest -q`), and the canary-isolation smoke test (`scripts/smoke_check.py`).

The smoke test is fully offline and proves that no minted canary ever reaches output artifacts. Expected: `status: pass`.

## Canary-isolation smoke

Run manually:
```bash
python scripts/smoke_check.py --config configs/preliminary_evidence.yaml
```
Outputs: `outputs/smoke_check.json` with counts (canaries generated, canaries found in outputs, leaks). Any non-zero leak count causes non-zero exit.

## Reproducing preliminary evidence (synthetic)

```bash
python scripts/run_synthetic_demo.py --config configs/synthetic_demo.yaml
# or
make demo
```
Outputs go to `outputs/synthetic_demo/` (not committed; excluded by `.gitignore`).

## Known limitations (artifact scope)

- The full OS-level prototype requires AOSP patching and OEM integration; that is outside the scope of this artifact package.
- Device experiments (B0–B3) require Android hardware/emulator setup and are run manually via the device workflow (`.github/workflows/device.yml`, `workflow_dispatch`).
- Any result tables marked TODO/N/A in the manuscript correspond to planned measurements; the artifact does not fabricate measured values.

## License

TBD: choose and record a license for the artifact (code, configs, schemas, and analysis scripts) before submission. See #323 in the checklist.

## Artifact evaluation

MobiSys artifact evaluation is optional; this appendix is provided for reproducibility. If artifact evaluation is requested, the one-command offline checks above satisfy the functional check; additional instructions for hardware-dependent stages are documented in `docs/reproducibility.md`.
