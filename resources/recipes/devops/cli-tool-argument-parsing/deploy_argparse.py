import argparse


def main():
    parser = argparse.ArgumentParser(description="Deploy CLI tool")
    parser.add_argument(
        "environment", choices=["dev", "staging", "prod"], help="Target environment"
    )
    parser.add_argument("--version", default="latest", help="App version to deploy")
    parser.add_argument("--dry-run", action="store_true", help="Simulate without changes")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()
    print(f"Deploying {args.version} to {args.environment}")
    if args.dry_run:
        print("(dry run mode)")


if __name__ == "__main__":
    main()
