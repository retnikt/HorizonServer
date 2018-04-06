import http.server
import json


class Horizon(http.server.HTTPServer):
    def __init__(self, config_dir):
        # default address to bind to
        address = ("0.0.0.0", 80)

        try:
            with open(f"{config_dir}/horizon.json") as f:
                self.config = json.load(f)
        except FileNotFoundError:
            # create config file
            pass
        # noinspection PyBroadException
        try:
            open(f"{config_dir}/horizon.json", 'x').close()
            self.config = {}
        except OSError as e:
            print(f"OSError {e.errno}: Could not create Horizon configuration file.")
            exit(e.errno)
        except Exception as e:
            # print error info
            print(f"{type(e).__name__}: {' '.join([str(i) for i in e.args])}")

        super(Horizon, self).__init__(address, HorizonHandler)


class HorizonHandler(http.server.BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super(HorizonHandler, self).__init__(*args, **kwargs)


if __name__ == "__main__":
    server = Horizon("horizon/")
    server.serve_forever()
