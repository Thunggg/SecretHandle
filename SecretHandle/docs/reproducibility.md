# Reproducibility

## Determinism

- One integer seed controls synthetic canaries, identifiers, and trial selection.
- HMAC test keys are derived from the seed only in synthetic mode.
- Synthetic latency is a deterministic surrogate and is labeled non-empirical.
- Confidence-interval resampling and paired permutation accept explicit seeds.
- JSON is sorted; configs are captured with SHA-256; per-trial outputs never contain canaries.

## Provenance

Each run records the public config, config hash, Python and platform versions, seed, real/synthetic flag, and the statement that paper placeholders were not used. Real runs must extend this with git commit, AOSP commit, device build/kernel, APK hashes, agent/model versions, prompt hashes, policy hashes, and endpoint manifest.

## Reproduction commands

```bash
python3 -m pytest -q
python3 scripts/run_synthetic_demo.py --config configs/synthetic_demo.yaml
python3 scripts/make_plots.py --input outputs/synthetic_demo/metrics.csv --output outputs/synthetic_demo/plots
python3 scripts/run_experiment.py --config configs/synthetic_demo.yaml --stage killer
```

Compare semantic trial JSON after excluding environment-specific provenance paths. Fixed-seed unit tests exercise this requirement.

## Integrity

Plots read `metrics.csv`; metrics are derived from `trials.jsonl`; no table or figure contains hard-coded paper outcomes. The result-integrity audit identifies every shipped generated artifact.
