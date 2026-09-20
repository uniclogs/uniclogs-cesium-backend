from __future__ import annotations

from os import getenv

from flask import Flask
from flask_cors import CORS

from .data import Data, GroundStation, Satellite
from .views import view_czml, view_groundstation, view_passes, view_satellite, view_tiles

DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 9000
DEFAULT_API_PREFIX = "/"
DEFAULT_DATA_DIR = getenv("DATA_DIR", "../data")

SATELLITES = [
    # Satellite('OreSat0', 52017, '2022-026'),
    Satellite("OreSat0.5", 60525, "2024-149"),
]

GROUND_STATIONS = [
    GroundStation("UniClOGS EB", 45.509054, -122.681394, 50, 0),
]


class App(Flask):
    host: str
    port: int
    data_dir: str
    debug: bool

    def __init__(
        self: App,
        data: Data,
        api_prefix: str = DEFAULT_API_PREFIX,
        debug: bool = False,
    ):
        super().__init__(__name__)

        # Setup app parameters
        self.data = data
        self.debug = debug

        # Register app views
        self.register_blueprint(view_czml, url_prefix=f"{api_prefix}/czml")
        self.register_blueprint(view_groundstation, url_prefix=f"{api_prefix}/gs")
        self.register_blueprint(view_passes, url_prefix=f"{api_prefix}/passes")
        self.register_blueprint(view_satellite, url_prefix=f"{api_prefix}/sat")
        self.register_blueprint(view_tiles, url_prefix=f"{api_prefix}/tiles")


def build_app(*args) -> App:
    app = App(
        data=Data(
            satellites=SATELLITES,
            groundstations=GROUND_STATIONS,
        )
    )

    ALLOWED_ORIGINS: list[str] = [
        "http://127.0.0.1:3000",
        "http://:localhost:3000",
        "https://cesium.uniclogs.org",
    ]
    CORS(app=app, origins=ALLOWED_ORIGINS)
    return app
