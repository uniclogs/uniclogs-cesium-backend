from flask import Blueprint, current_app

view_passes = Blueprint("view_passes", __name__)


@view_passes.route("/<groundstation>/<satellite>")
def get_passes_by_gs_sat(groundstation: str, satellite: str):
    passes = {}
    data = current_app.data

    gs_passes = data.passes.get(groundstation)
    if gs_passes is None:
        return {"err": f"No pases found for {groundstation}!"}, 404

    sat_passes = gs_passes.get(satellite)
    if sat_passes is None:
        return {"err": f"No passes for {satellite} over {groundstation}!"}, 404

    return [p.to_dict() for p in sat_passes], 201
