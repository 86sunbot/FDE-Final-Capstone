.PHONY: test legacy-test demo app evaluate verify

test:
	python -m pytest -q

legacy-test:
	python tools/run_legacy_baseline_tests.py

demo:
	PYTHONPATH=src python -m fde_capstone.cli demo --db runtime/capstone.db

app:
	PYTHONPATH=src python -m uvicorn fde_capstone.api:app --host 127.0.0.1 --port 8000

evaluate:
	PYTHONPATH=src python -m fde_capstone.cli evaluate --db runtime/evaluation.db --output reports/generated/evaluation-results.json

verify:
	python tools/verify_final_capstone.py
