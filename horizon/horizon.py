import http.server


class Horizon(http.server.HTTPServer):
    def __init__(self):
        address = ("0.0.0.0", 80)
        super(Horizon, self).__init__(address, HorizonHandler)


class HorizonHandler(http.server.BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super(HorizonHandler, self).__init__(*args, **kwargs)


if __name__ == "__main__":
    server = Horizon()
    server.serve_forever()

