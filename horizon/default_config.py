DEFAULT_CONFIG = """{
  "horizon": {
    "logging": {
      "level": "warning"
    },
    "server": {
      "listen": "0.0.0.0",
      "port": 80
    },
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
"""