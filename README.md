# Python Network Scanner

A multithreaded, legal-use network scanner built with Python.  
Scans IP addresses and port ranges across subnets, ranges, or single hosts, then outputs clean reports in TXT, CSV, and JSON formats.

---

## Features

- TCP connect scanning (safe and fully cross-platform)
- Input support:
  - Single IP (e.g., `192.168.1.10`)
  - CIDR block (e.g., `192.168.1.0/24`)
  - IP range (e.g., `192.168.1.10-192.168.1.20`)
- Custom port ranges and lists (e.g., `22,80,443` or `1-1024`)
- Multithreaded performance with adjustable thread count
- Generates timestamped reports in:
  - `scan_reports/*.txt`
  - `scan_reports/*.csv`
  - `scan_reports/*.json`
- Includes full unit test suite (`unittest`)

---

## Usage

### Requirements

This project uses only Python's standard library — no external packages required.

### Run a basic scan

```bash
python scan.py 192.168.1.1
