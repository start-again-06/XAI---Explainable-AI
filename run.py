#!/usr/bin/env python3
"""Project launcher entrypoint.

This script reuses the existing startup flow defined in start.py and adds a
clean terminal-friendly link view.
"""

import argparse

from start import main as start_main, print_local_links


def parse_args() -> argparse.Namespace:
    """Parse CLI options for launcher behavior."""
    parser = argparse.ArgumentParser(description="Run XAI-IDS")
    parser.add_argument(
        "--links",
        action="store_true",
        help="Print localhost links and exit without starting services.",
    )
    return parser.parse_args()


def main() -> int:
    """Main launcher flow."""
    args = parse_args()
    print_local_links()

    if args.links:
        return 0

    return start_main()


if __name__ == "__main__":
    raise SystemExit(main())