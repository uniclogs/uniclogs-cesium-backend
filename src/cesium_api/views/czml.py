from json import loads

from flask import Blueprint, current_app

view_czml = Blueprint("view_czml", __name__)


@view_czml.route("/", methods=["GET"])
def get_root():
    cz = current_app.data.czml
    while len(cz) == 0:
        cz = current_app.data.czml
    return loads(cz)
