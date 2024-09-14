from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path


class Serv(BaseHTTPRequestHandler):
    def do_GET(self):
        with Path("src/frontend/index.html").open() as ff:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes(ff.read(), "utf-8"))


def main():
    httpd = HTTPServer(("localhost", 8080), Serv)
    httpd.serve_forever()
