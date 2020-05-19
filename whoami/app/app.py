"""Flask app that returns information on its current environment at /api/whoami"""

from typing import Any

from flask import Flask, jsonify

from lib.whoami import Whoami

APP = Flask(__name__)
APP.config["JSONIFY_PRETTYPRINT_REGULAR"] = True

whoami = Whoami()


@APP.route("/")
def _index() -> str:
    # Confirms the app is reachable
    return "Working"


@APP.route("/api/mac")
def _get_mac() -> str:
    # Maps the MAC address to /api/mac
    return whoami.get_mac()


@APP.route("/api/whoami")
def _get_whoami() -> Any:
    # Maps the whoami output to /api/whoami
    return jsonify(whoami.to_json())


if __name__ == "__main__":
    # For testing/debugging
    APP.run()
