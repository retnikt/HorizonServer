import http.server
import json
import shutil
from datetime import datetime
from horizon.default_config import DEFAULT_CONFIG
from horizon.util import *
import logging


class Horizon(http.server.HTTPServer):
    def __init__(self, config_dir, log_level=logging.WARNING, log_file="/var/log/horizon.log"):

        self.logger = logging.getLogger("Horizon@{address[0]}:{address[1]}")
        self.logger.setLevel(log_level)
        self.logger.addHandler(logging.FileHandler(log_file))
        # also log to stderr
        self.logger.addHandler(logging.StreamHandler())

        self.config = AttrDict(json.loads(DEFAULT_CONFIG))
        self.config_dir = config_dir
        self.config = AttrDict(self.load_config())
        super(Horizon, self).__init__(self.config.server.address, HorizonHandler)

    def load_config(self):
        try:
            with open(f"{self.config_dir}/horizon.json") as f:
                return json.load(f)
        except FileNotFoundError:
            self.create_config()
        except json.JSONDecodeError:
            self.logger.error("Failed to read Horizon configuration.")

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
            self.logger.critical(f"OSError {e.errno}: Could not create Horizon configuration file.")
            exit(e.errno)
        except Exception as e:
            # log error info
            self.logger.critical(f"{type(e).__name__}: {' '.join([str(i) for i in e.args])}")
            exit(1)


class HorizonHandler(http.server.BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super(HorizonHandler, self).__init__(*args, **kwargs)


if __name__ == "__main__":
    server = Horizon("horizon/")
    server.serve_forever()
