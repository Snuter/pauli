#!/usr/bin/env python3
"""Serve the static ui-mockup on the local network.

Binds to 0.0.0.0 so other machines in the network can open the mockup
via this machine's LAN IP. Stdlib only.

Usage:
    python start_server.py [--host 0.0.0.0] [--port 8000]
"""

import argparse
import socket
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


def lan_ips() -> list[str]:
    """Best-effort list of local IPv4 addresses for printing URLs."""
    ips: set[str] = set()
    try:
        _, _, addrs = socket.gethostbyname_ex(socket.gethostname())
        ips.update(addrs)
    except socket.gaierror:
        pass
    try:
        # UDP connect does not send packets; reveals the outbound interface IP.
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            ips.add(s.getsockname()[0])
    except OSError:
        pass
    ips.discard("127.0.0.1")
    return sorted(ips)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="0.0.0.0", help="Bind address (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8000, help="Port (default: 8000)")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent
    handler = partial(SimpleHTTPRequestHandler, directory=str(root))
    server = ThreadingHTTPServer((args.host, args.port), handler)

    host_label = args.host if args.host != "0.0.0.0" else "localhost"
    print(f"Serving {root} at http://{host_label}:{args.port}/")
    if args.host == "0.0.0.0":
        for ip in lan_ips():
            print(f"Network: http://{ip}:{args.port}/")
        if not lan_ips():
            print("(Could not determine LAN IP; use this machine's IP manually.)")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
