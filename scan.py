# scan.py

import argparse
import os
from scanner.core import run_scan
from scanner.utils import parse_targets, parse_ports, legal_warning
from scanner.report import save_report


def main():
    parser = argparse.ArgumentParser(
        description="Python Network Scanner (for legal and educational use only)"
    )
    parser.add_argument("target", help="Target IP, range (192.168.1.1-10), or CIDR (192.168.1.0/24)")
    parser.add_argument(
        "--ports", default="1-1024",
        help="Port range to scan (e.g. 22,80,443 or 1-1024,8080)"
    )
    parser.add_argument(
        "--threads", type=int, default=100,
        help="Number of concurrent threads (default: 100)"
    )
    parser.add_argument(
        "--formats", nargs="+", choices=["txt", "json", "csv"], default=["txt", "json", "csv"],
        help="Report formats to save (default: all)"
    )

    args = parser.parse_args()

    # Display legal disclaimer
    legal_warning()

    # Parse and validate inputs
    targets = parse_targets(args.target)
    ports = parse_ports(args.ports)

    print(f"\nStarting scan on {len(targets)} host(s), scanning {len(ports)} port(s) each...")

    # Run scan
    results = run_scan(targets, ports, max_threads=args.threads)

    # Ensure output directory exists
    os.makedirs("scan_reports", exist_ok=True)

    # Save results in requested formats
    for fmt in args.formats:
        save_report(results, format=fmt)

    print("\nScan complete. Reports saved in ./scan_reports/")


if __name__ == "__main__":
    main()
