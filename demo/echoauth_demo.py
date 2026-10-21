"""Non-authoritative EchoAuth demonstration. No production runtime integration."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os

def evaluate(path, method):
    if method == "GET" and path == "/api/health":
        return 200, {"status": "demo_only", "runtime": "unavailable", "authorization_enabled": False}
    if method == "POST" and path == "/api/v1/authorize":
        return 503, {"decision": "HOLD", "reason": "RUNTIME_UNAVAILABLE", "authorized": False, "mode": "demo_only"}
    if method == "GET" and path == "/":
        return 200, {"service": "EchoAuth bounded demonstration", "mode": "demo_only", "authority": "none", "runtime": "unavailable"}
    return 404, {"error": "not_found"}

class Handler(BaseHTTPRequestHandler):
    def respond(self, method):
        status, body = evaluate(self.path.split("?")[0], method)
        data = json.dumps(body).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        self.respond("GET")

    def do_POST(self):
        self.respond("POST")

if __name__ == "__main__":
    ThreadingHTTPServer(("0.0.0.0", int(os.environ.get("PORT", "8000"))), Handler).serve_forever()
