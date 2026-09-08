"""argparse example: basic flags, typed options, and subcommands."""

import argparse


def build_parser():
    parser = argparse.ArgumentParser(prog="mytool", description="Process files.")
    parser.add_argument("input", help="Input file path")
    parser.add_argument("-o", "--output", default="out.txt", help="Output file path")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose logging")
    parser.add_argument("--count", type=int, default=1, help="Repeat count")

    sub = parser.add_subparsers(dest="command")
    push = sub.add_parser("push", help="Push to remote")
    push.add_argument("--force", action="store_true", help="Force push")

    pull = sub.add_parser("pull", help="Pull from remote")
    pull.add_argument("--depth", type=int, default=1, help="Clone depth")

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    return args


if __name__ == "__main__":
    args = main()
    print(f"Input: {args.input}, Output: {args.output}, Verbose: {args.verbose}")
