from pathlib import Path

def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]

def db_path() -> Path:
    return repo_root() / "data" / "cgt_legacy.db"
