from json import dumps

from flask import Blueprint, current_app

from ..data import Data

view_satellite = Blueprint("view_satellite", __name__)


@view_satellite.route("/", methods=["GET"])
def get_sat_names():
    data: Data = current_app.data
    return dumps([s.name for s in data.satellites])


@view_satellite.route("/<name>", methods=["GET"])
def get_sat_info(name: str):
    data: Data = current_app.data
    match = list(filter(lambda s: s.name.lower() == name.lower(), data.satellites))

    if not match:
        return {"err": f'No satellite matching "{name}" found'}, 404
    else:
        return match[0].to_dict(), 200
