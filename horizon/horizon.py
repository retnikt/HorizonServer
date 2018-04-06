import http.server

if __name__ == "__main__":
    server = http.server.HTTPServer(("0.0.0.0", 80), http.server.BaseHTTPRequestHandler)
    server.serve_forever()

