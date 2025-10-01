# scanner/core.py

import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime


def scan_port(host, port, timeout=1.0):
    """
    Attempt to connect to a given port on a host.
    Returns True if open, False otherwise.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        try:
            sock.connect((host, port))
            return True
        except (socket.timeout, ConnectionRefusedError, OSError):
            return False


def scan_host(host, ports, timeout=1.0):
    """
    Scans a list of ports on a single host.
    Returns a dict: { "host": ..., "open_ports": [...] }
    """
    open_ports = []
    for port in ports:
        if scan_port(host, port, timeout=timeout):
            open_ports.append(port)
    return {"host": host, "open_ports": open_ports}


def run_scan(targets, ports, max_threads=100, timeout=1.0):
    """
    Main scanning routine.
    Returns a list of result dicts: [{host: ..., open_ports: [...]}, ...]
    """
    results = []
    start_time = datetime.now()

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        future_to_host = {
            executor.submit(scan_host, host, ports, timeout): host for host in targets
        }

        for future in as_completed(future_to_host):
            host = future_to_host[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                results.append({"host": host, "open_ports": [], "error": str(e)})

    duration = (datetime.now() - start_time).total_seconds()
    print(f"\nScan finished in {duration:.2f} seconds.")

    return results
