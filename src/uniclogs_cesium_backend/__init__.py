from importlib.metadata import metadata

from uniclogs_cesium_backend.app import App

from .app import GROUND_STATIONS, SATELLITES, build_app

__metadata__ = metadata(__name__)

APP_NAME: str = __metadata__["name"]
APP_DESCRIPTION: str = __metadata__["description"]
APP_VERSION: str = __metadata__["version"]

application: App = build_app()

__all__ = ["application", "SATELLITES", "GROUND_STATIONS"]
