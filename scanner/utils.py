# scanner/utils.py

import ipaddress


def legal_warning():
    print("WARNING: This tool is intended for scanning networks you own or have explicit permission to scan.")
    print("Unauthorized scanning may be illegal and could result in consequences.")
    print("Use responsibly.\n")


def parse_targets(target_input):
    """
    Accepts:
        - Single IP: 192.168.1.1
        - CIDR: 192.168.1.0/24
        - IP range: 192.168.1.10-192.168.1.20
    Returns:
        List of IP strings
    """
    targets = []

    # IP range
    if "-" in target_input:
        start_ip, end_ip = target_input.split("-")
        start_ip = ipaddress.IPv4Address(start_ip.strip())

        # If end_ip is short form (e.g. just last octet), expand it
        if "." not in end_ip:
            prefix = ".".join(str(start_ip).split(".")[:3])
            end_ip = f"{prefix}.{end_ip.strip()}"

        end_ip = ipaddress.IPv4Address(end_ip.strip())

        if end_ip < start_ip:
            raise ValueError("End IP must be greater than or equal to start IP in range.")

        for ip_int in range(int(start_ip), int(end_ip) + 1):
            targets.append(str(ipaddress.IPv4Address(ip_int)))

    # CIDR
    elif "/" in target_input:
        try:
            network = ipaddress.IPv4Network(target_input, strict=False)
            targets = [str(ip) for ip in network.hosts()]
        except ValueError:
            raise ValueError("Invalid CIDR notation.")

    # Single IP
    else:
        try:
            ipaddress.IPv4Address(target_input)
            targets = [target_input]
        except ValueError:
            raise ValueError("Invalid IP address.")

    return targets


def parse_ports(port_input):
    """
    Accepts:
        - Single ports: 22,80
        - Ranges: 1-1024,8080-8090
    Returns:
        Sorted list of unique ports (integers)
    """
    ports = set()
    parts = port_input.split(",")

    for part in parts:
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            try:
                start, end = map(int, part.split("-"))
                ports.update(range(start, end + 1))
            except ValueError:
                continue
        else:
            try:
                port = int(part)
                ports.add(port)
            except ValueError:
                continue

    return sorted(p for p in ports if 1 <= p <= 65535)
