import logging
from argparse import ArgumentParser, Namespace

from flask_cors import CORS

from . import (
    APP_DESCRIPTION,
    APP_NAME,
    APP_VERSION,
    DEFAULT_API_PREFIX,
    DEFAULT_DATA_DIR,
    DEFAULT_HOST,
    DEFAULT_PORT,
    GROUND_STATIONS,
    SATELLITES,
)
from .app import App
from .data import Data

LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def parse_args() -> Namespace:
    parser = ArgumentParser(prog=APP_NAME, description=APP_DESCRIPTION)
    parser.add_argument(
        "--version",
        "-v",
        dest="version",
        action="store_true",
        default=False,
        help="Print application version.",
    )
    parser.add_argument(
        "-H",
        "--host",
        dest="host",
        type=str,
        default=DEFAULT_HOST,
        help="Host to bind API server to. (default %(default)s)",
    )
    parser.add_argument(
        "-P",
        "--port",
        dest="port",
        type=int,
        default=DEFAULT_PORT,
        help="Host to bind API server to. (default %(default)s)",
    )
    parser.add_argument(
        "--debug",
        dest="debug",
        action="store_true",
        default=False,
        help="Enable debug mode for the API. (default: %(default)s)",
    )
    parser.add_argument(
        "--data-dir",
        "-d",
        dest="data_dir",
        type=str,
        default=DEFAULT_DATA_DIR,
        help="Data directory with all of the generated globe tiles. (default: %(default)s)",
    )
    parser.add_argument(
        "--prefix",
        "-p",
        dest="api_prefix",
        type=str,
        default=DEFAULT_API_PREFIX,
        metavar="API Prefix",
        help="API Prefix to append to all endpoints. (default: %(default)s)",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    if args.version:
        print(f"{APP_NAME} v{APP_VERSION}: {APP_DESCRIPTION}")
        return

    api_prefix = args.api_prefix[:-1] if args.api_prefix.endswith("/") else args.api_prefix

    app = App(
        data=Data(SATELLITES, GROUND_STATIONS),
        host=args.host,
        port=args.port,
        api_prefix=api_prefix,
        data_dir=args.data_dir,
        debug=args.debug,
    )
    allowed_hosts = ["http://:localhost:3000", "https://cesium-api.uniclogs.org"]
    CORS(app, origins=allowed_hosts)
    return app


app = main()
