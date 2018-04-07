import http.server
import json
import shutil
from datetime import datetime
from horizon.default_config import DEFAULT_CONFIG
from horizon.util import *
import logging
import ssl


class Horizon(http.server.HTTPServer):
    def __init__(self, config_dir, log_level=logging.WARNING, log_file="/var/log/horizon.log"):

        self.logger = logging.getLogger("Horizon@{address[0]}:{address[1]}")
        self.logger.setLevel(log_level)
        self.logger.addHandler(logging.FileHandler(log_file))
        # also log to stderr
        self.logger.addHandler(logging.StreamHandler())

        # load config
        self.config = json.loads(DEFAULT_CONFIG)['horizon']
        self.config_dir = config_dir
        self.config = self.load_config()['horizon']

        # init super class
        super(Horizon, self).__init__((self.config['server']['listen'], self.config['server']['port']),
                                      HorizonHandler)

        if self.config.ssl.enabled:
            self.socket = ssl.wrap_socket(self.socket, certfile=self.config['ssl']['cert-path'],
                                          keyfile=self.config['ssl']['key-path'], server_side=True)

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
