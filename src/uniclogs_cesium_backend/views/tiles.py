from os.path import abspath, exists

from flask import Blueprint, current_app, send_file

view_tiles = Blueprint("view_tiles", __name__)


@view_tiles.route("/<int:zoom>/<int:x>/<int:y>.png")
def get_tile(zoom: int, x: int, y: int):
    data_dir = current_app.data_dir
    tile_path = abspath(f"{data_dir}/tiles/{zoom}/{x}/{y}.png")

    try:
        exists(tile_path)
        return send_file(tile_path)
    except FileNotFoundError:
        return {"err": f"No such tile for {x} by {y} at a zoom of {zoom}"}, 404
