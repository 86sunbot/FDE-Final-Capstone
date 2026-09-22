from __future__ import annotations

import argparse
import json

from .application import CapstoneApplication
from .demo import run_demo


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description="Synthetic CGT FDE capstone")
    commands = root.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init")
    init.add_argument("--db", required=True)
    demo = commands.add_parser("demo")
    demo.add_argument("--db", required=True)
    demo.add_argument("--ai-mode", choices=["off", "fake"], default="off")
    evaluate = commands.add_parser("evaluate")
    evaluate.add_argument("--db", required=True)
    evaluate.add_argument("--output", required=True)
    backup = commands.add_parser("backup")
    backup.add_argument("--db", required=True)
    backup.add_argument("--output", required=True)
    return root


def main() -> None:
    args = parser().parse_args()
    if args.command == "init":
        app = CapstoneApplication(args.db)
        app.close()
        print(json.dumps({"status": "initialized", "db": args.db}))
    elif args.command == "demo":
        print(json.dumps(run_demo(args.db, args.ai_mode), indent=2))
    elif args.command == "evaluate":
        from .evaluation import run_catalog

        result = run_catalog(args.db, args.output)
        print(json.dumps(result["summary"], indent=2))
    elif args.command == "backup":
        app = CapstoneApplication(args.db)
        destination = app.db.backup(args.output)
        digest = app.db.state_digest()
        app.close()
        print(json.dumps({"status": "backed_up", "path": str(destination), "source_state_digest": digest}))


if __name__ == "__main__":
    main()
