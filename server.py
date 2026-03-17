#!/usr/bin/env python3
"""
Simple HTTP server to run the Prigogine quotes app
"""
import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

PORT = 8000
HANDLER = http.server.SimpleHTTPRequestHandler

def start_server():
    os.chdir(Path(__file__).parent)

    with socketserver.TCPServer(("", PORT), HANDLER) as httpd:
        url = f"http://localhost:{PORT}"
        print(f"\n✨ Prigogine Quotes App is running!")
        print(f"📍 Open your browser: {url}")
        print(f"🛑 Press Ctrl+C to stop the server\n")

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n✋ Server stopped.")

if __name__ == "__main__":
    start_server()
