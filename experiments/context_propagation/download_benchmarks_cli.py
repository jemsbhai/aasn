"""CLI for downloading canonical benchmarks.

Usage:
    python download_benchmarks_cli.py --tier 1          # Download tier 1 benchmarks
    python download_benchmarks_cli.py --all             # Download all available
    python download_benchmarks_cli.py --list            # List available benchmarks
    python download_benchmarks_cli.py --name humaneval  # Download specific benchmark
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from harness.download_benchmarks import BenchmarkDownloader


def main():
    parser = argparse.ArgumentParser(description="Download canonical benchmarks")
    parser.add_argument("--tier", type=int, default=1, help="Max tier to download (1-3)")
    parser.add_argument("--all", action="store_true", help="Download all available benchmarks")
    parser.add_argument("--name", type=str, help="Download a specific benchmark by name")
    parser.add_argument("--list", action="store_true", help="List available benchmarks")
    parser.add_argument("--force", action="store_true", help="Re-download even if cached")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parent / "benchmarks",
        help="Output directory for benchmark files",
    )

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    downloader = BenchmarkDownloader(cache_dir=args.output_dir)

    if args.list:
        print("\nAvailable benchmarks:\n")
        for info in downloader.list_available():
            cached = "  [cached]" if info["name"] in downloader.list_cached() else ""
            print(f"  Tier {info['tier']} | {info['name']:20s} | {info['category']:10s} | {info['description']}{cached}")
        print()
        return

    if args.name:
        path = downloader.download(args.name, force=args.force)
        print(f"Downloaded: {path}")
        return

    tier = 3 if args.all else args.tier
    paths = downloader.download_all(tier=tier, force=args.force)
    print(f"\nDownloaded {len(paths)} benchmarks:")
    for name, path in paths.items():
        print(f"  {name}: {path}")


if __name__ == "__main__":
    main()
