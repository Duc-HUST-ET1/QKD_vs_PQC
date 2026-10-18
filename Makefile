.PHONY: test qkd pqc analysis all

test:
	python -m pytest

qkd:
	python scripts/run_qkd.py

pqc:
	python scripts/run_pqc_benchmark.py

analysis:
	python scripts/run_analysis.py

all:
	python scripts/run_all.py
