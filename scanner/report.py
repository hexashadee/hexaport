# scanner/report.py

import json
import csv
from datetime import datetime
import os


def _generate_filename(extension):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join("scan_reports", f"scan_report_{timestamp}.{extension}")


def save_report(results, format="txt"):
    if format == "txt":
        _save_txt(results)
    elif format == "csv":
        _save_csv(results)
    elif format == "json":
        _save_json(results)
    else:
        raise ValueError(f"Unsupported report format: {format}")


def _save_txt(results):
    filename = _generate_filename("txt")
    with open(filename, "w") as f:
        for entry in results:
            host = entry.get("host")
            open_ports = entry.get("open_ports", [])
            f.write(f"Host: {host}\n")
            if open_ports:
                f.write(f"Open Ports: {', '.join(map(str, open_ports))}\n")
            else:
                f.write("Open Ports: None\n")
            f.write("-" * 40 + "\n")
    print(f"Text report saved: {filename}")


def _save_csv(results):
    filename = _generate_filename("csv")
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Host", "Open Ports"])
        for entry in results:
            host = entry.get("host")
            open_ports = ",".join(map(str, entry.get("open_ports", [])))
            writer.writerow([host, open_ports])
    print(f"CSV report saved: {filename}")


def _save_json(results):
    filename = _generate_filename("json")
    with open(filename, "w") as f:
        json.dump(results, f, indent=4)
    print(f"JSON report saved: {filename}")
