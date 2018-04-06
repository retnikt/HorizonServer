import http.server
import json
import shutil
from datetime import datetime
from horizon.default_config import DEFAULT_CONFIG


class Horizon(http.server.HTTPServer):
    def __init__(self, config_dir):

        self.config = {}
        self.config_dir = config_dir
        self.load_config()

        # default address to bind to
        address = ("0.0.0.0", 80)
        super(Horizon, self).__init__(address, HorizonHandler)

    def load_config(self):
        try:
            with open(f"{self.config_dir}/horizon.json") as f:
                self.config = json.load(f)
        except FileNotFoundError:
            self.create_config()
        except json.JSONDecodeError:
            print("Failed to read Horizon configuration.")
            # copy broken configuration
            shutil.copy2(f"{self.config_dir}/horizon.json",
                         f"{self.config_dir}/horizon-broken-{datetime.now():%Y-%m-%d-%H-%M}.json")
            # create new config
            self.create_config()

    # noinspection PyBroadException
    def create_config(self):
        try:
            # write defaults to config file
            with open(f"{self.config_dir}/horizon.json", 'w') as f:
                f.write(DEFAULT_CONFIG)
        except OSError as e:
            print(f"OSError {e.errno}: Could not create Horizon configuration file.")
            exit(e.errno)
        except Exception as e:
            # print error info
            print(f"{type(e).__name__}: {' '.join([str(i) for i in e.args])}")
            exit(1)


class HorizonHandler(http.server.BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super(HorizonHandler, self).__init__(*args, **kwargs)


if __name__ == "__main__":
    server = Horizon("horizon/")
    server.serve_forever()
