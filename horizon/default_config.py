DEFAULT_CONFIG = """{
  "horizon": {
    "server": {
      "listen": "0.0.0.0",
      "port": 80
    },
    "global": {},
    "domains": {
      "default": {
        "webroot": "/var/horizon/www/",
        "ssl": {
          "enabled": false,
          "redirect": "none",
          "cert-path": "",
          "key-path": "",
          "ca": {
            "chain-path": null,
            "cert-path": null,
            "revocation-path": null
          }
        }
      }
    }
  }
}
"""