.PHONY: test legacy-test demo evaluate verify

test:
	python -m pytest -q

legacy-test:
	python tools/run_legacy_baseline_tests.py

demo:
	PYTHONPATH=src python -m fde_capstone.cli demo --db runtime/capstone.db

evaluate:
	PYTHONPATH=src python -m fde_capstone.cli evaluate --db runtime/evaluation.db --output reports/generated/evaluation-results.json

verify:
	python tools/verify_final_capstone.py
