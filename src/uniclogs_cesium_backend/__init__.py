from importlib.metadata import metadata

from .app import GROUND_STATIONS, SATELLITES, uniclogs_cesium_backend

__metadata__ = metadata(__name__)

APP_NAME: str = __metadata__["name"]
APP_DESCRIPTION: str = __metadata__["description"]
APP_VERSION: str = __metadata__["version"]

__all__ = ["uniclogs_cesium_backend", "SATELLITES", "GROUND_STATIONS"]
