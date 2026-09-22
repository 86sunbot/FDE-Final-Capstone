import argparse, json
from .diagnostics import run_diagnostics


def main():
    parser=argparse.ArgumentParser(description="CGT brownfield utilities")
    sub=parser.add_subparsers(dest='command', required=True)
    sub.add_parser('diagnostics')
    args=parser.parse_args()
    if args.command=='diagnostics':
        print(json.dumps(run_diagnostics(), indent=2))

if __name__ == '__main__':
    main()
