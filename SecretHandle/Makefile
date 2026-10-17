PYTHON ?= python3
CONFIG ?= configs/synthetic_demo.yaml
SMOKE_CONFIG ?= configs/preliminary_evidence.yaml

.PHONY: install test lint typecheck smoke evidence demo plots killer check ci clean-generated

install:
	$(PYTHON) -m pip install -e ".[dev]"

test:
	$(PYTHON) -m pytest -q

lint:
	$(PYTHON) -m ruff check .

typecheck:
	$(PYTHON) -m mypy src

# One-command offline canary-isolation smoke: runs the synthetic pipeline and
# proves no minted canary ever reaches an output artifact.
smoke:
	$(PYTHON) scripts/smoke_check.py --config $(SMOKE_CONFIG)

evidence:
	$(PYTHON) scripts/run_experiment.py --config $(SMOKE_CONFIG) --stage killer

demo:
	$(PYTHON) scripts/run_synthetic_demo.py --config $(CONFIG)

plots:
	$(PYTHON) scripts/make_plots.py --input outputs/synthetic_demo/metrics.csv --output outputs/synthetic_demo/plots

killer:
	$(PYTHON) scripts/run_experiment.py --config $(CONFIG) --stage killer

check: lint typecheck test smoke
	@echo "All checks passed (lint, typecheck, tests, canary smoke)."

ci: check

clean-generated:
	@echo "Generated outputs are intentionally not deleted automatically; remove a specific run directory manually."
