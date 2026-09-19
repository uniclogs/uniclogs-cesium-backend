from flask import Blueprint, current_app

from ..data import Data

view_groundstation = Blueprint("view_groundstation", __name__)


@view_groundstation.route("/")
def get_root():
    data: Data = current_app.data
    return [gs.name for gs in data.groundstations], 200


@view_groundstation.route("/<name>")
def get_gs_by_name(name: str):
    data: Data = current_app.data
    match = list(filter(lambda g: g.name == name, data.groundstations))

    if len(match) == 1:
        return match[0].to_dict()
    else:
        return {"err": f'No ground station matching "{name}"'}, 404
