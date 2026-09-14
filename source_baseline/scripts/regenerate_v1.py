"""Deterministic v1 regeneration helper.

This repository ships with pre-generated CSV/JSONL/SQLite data. The original full generator logic is stored
in `tools/v1_dataset_builder.py`. Running that file rebuilds the v1 snapshot in a sibling output directory.
"""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).resolve().parents[1]/'tools'/'v1_dataset_builder.py'), run_name='__main__')
