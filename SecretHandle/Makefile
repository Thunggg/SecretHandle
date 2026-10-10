PYTHON ?= python3
CONFIG ?= configs/synthetic_demo.yaml

.PHONY: test demo plots killer clean-generated

test:
	$(PYTHON) -m pytest -q

demo:
	$(PYTHON) scripts/run_synthetic_demo.py --config $(CONFIG)

plots:
	$(PYTHON) scripts/make_plots.py --input outputs/synthetic_demo/metrics.csv --output outputs/synthetic_demo/plots

killer:
	$(PYTHON) scripts/run_experiment.py --config $(CONFIG) --stage killer

clean-generated:
	@echo "Generated outputs are intentionally not deleted automatically; remove a specific run directory manually."
