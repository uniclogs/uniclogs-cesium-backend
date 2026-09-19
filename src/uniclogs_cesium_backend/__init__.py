from importlib.metadata import description, name, version

from .app import uniclogs_cesium_backend as app
from .data import GroundStation, Satellite

APP_NAME = name(__name__)
APP_DESCRIPTION = description(__name__)
APP_VERSION = version(__name__)

DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 9000
DEFAULT_API_PREFIX = "/"

SATELLITES = [
    # Satellite('OreSat0', 52017, '2022-026'),
    Satellite("OreSat0.5", 60525, "2024-149"),
]

GROUND_STATIONS = [
    GroundStation("UniClOGS EB", 45.509054, -122.681394, 50, 0),
]

__all__ = [
    "app"
]