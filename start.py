#!/usr/bin/env python3
"""One-command local launcher for the static demo page."""

from __future__ import annotations

import argparse
import contextlib
import http.server
import socket
import socketserver
import webbrowser
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


def pick_port(preferred: int) -> int:
    """Use preferred port when free, otherwise pick a random available one."""
    with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as probe:
        try:
            probe.bind(("127.0.0.1", preferred))
            return preferred
        except OSError:
            probe.bind(("127.0.0.1", 0))
            return int(probe.getsockname()[1])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Start a local server and open the VideoTube page in your browser."
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Preferred local port (default: 8000).",
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Start server without auto-opening the browser.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    port = pick_port(args.port)
    handler = http.server.SimpleHTTPRequestHandler

    with ReusableTCPServer(("127.0.0.1", port), handler) as httpd:
        url = f"http://127.0.0.1:{port}/index.html"
        print(f"Serving {PROJECT_ROOT} at {url}")
        print("Press Ctrl+C to stop.")

        if not args.no_browser:
            webbrowser.open(url)

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")


if __name__ == "__main__":
    main()
