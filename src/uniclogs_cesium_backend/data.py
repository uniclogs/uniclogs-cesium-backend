from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from threading import Thread
from time import sleep

import requests
from dataclasses_json import config, dataclass_json
from marshmallow import fields
from satellite_czml import satellite_czml
from skyfield.api import EarthSatellite, Loader, Topos, wgs84

ACTIVAE_SAT_URL = "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle"
INTDES_URL_BASE = "https://celestrak.org/NORAD/elements/gp.php?INTDES="

UPDATE_HOURS = 12

# pass settings
DAYS = 7
MIN_DURATION_S = 300
MIN_CUL_EL = 10


@dataclass_json
@dataclass(frozen=True)
class Satellite:
    name: str
    norad_catalog_number: int
    international_designator: str


@dataclass_json
@dataclass(frozen=True)
class GroundStation:
    name: str
    latitude_deg: float
    longitude_deg: float
    altitude_m: float
    horizon_deg: float = 0.0


@dataclass_json
@dataclass(frozen=True)
class OrbitalPass:
    aos_utc: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format="iso"),
        )
    )
    los_utc: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format="iso"),
        )
    )
    max_el: float = 0.0
    aos_az: float = 0.0
    los_az: float = 0.0


class Data:
    def __init__(self, satellites: list[Satellite], groundstations: list[GroundStation]):
        self.satellites = satellites
        self.groundstations = groundstations

        self.dt = datetime.utcnow()
        self.tles: list[list[str]] = []
        self.czml: str = ""
        self.passes: dict[GroundStation, list[OrbitalPass]] = {}

        self.thread = Thread(target=self._update, daemon=True)
        self.thread.start()

    def _update(self):
        while True:
            self._update_tles()
            self._update_czml()
            self._update_passes()
            sleep(UPDATE_HOURS * 60 * 60)

    def _update_tles(self):
        tles = []
        act_sats_tles = fetch_tles(ACTIVAE_SAT_URL)
        for sat in self.satellites:
            tle = ""

            if sat.norad_catalog_number in act_sats_tles:
                tle = act_sats_tles[sat.norad_catalog_number]
            else:
                intdes_tles = fetch_tles(INTDES_URL_BASE + sat.international_designator)
                if sat.norad_catalog_number in intdes_tles:
                    tle = intdes_tles[sat.norad_catalog_number]

            if tle != "":
                tle[0] = sat.name
                tles.append(tle)
        self.tles = tles

    def _update_czml(self):
        czml_raw = satellite_czml(
            tle_list=self.tles,
            start_time=self.dt,
            end_time=self.dt + timedelta(days=DAYS),
            speed_multiplier=1,
        ).get_czml()

        # fix clock to be real time
        czml_json = json.loads(czml_raw)
        czml_json[0]["clock"]["step"] = "SYSTEM_CLOCK"
        self.czml = json.dumps(czml_json)

    def _update_passes(self):
        for gs in self.groundstations:
            passes = {}
            for tle in self.tles:
                passes[tle[0]] = get_all_passes(tle, gs, self.dt, DAYS, MIN_DURATION_S)
            self.passes[gs.name] = passes


def fetch_tles(url: str) -> dict[int, list[str]]:
    """Fetch the TLEs from URL"""
    tles: dict[int, list[str]] = {}
    try:
        response = requests.get(url)
    except Exception:
        return tles

    if response.status_code != 200:
        return tles

    lines_raw = response.content.decode().split("\n")
    lines = [i.strip() for i in lines_raw]
    lines = lines[:-1]  # remove trailing empty line
    for i in range(0, len(lines), 3):
        cat_num = int(lines[i + 1][1:7])
        tles[cat_num] = lines[i : i + 3]
    return tles


def get_all_passes(
    tle: list[str],
    gs: GroundStation,
    start_datetime: datetime,
    days: int,
    min_duration_s: int = 0,
) -> list[OrbitalPass]:
    load = Loader("/tmp", verbose=False)
    ts = load.timescale()
    t0 = ts.utc(start_datetime.replace(tzinfo=timezone.utc))
    t1 = t0 + timedelta(days=days)

    loc = Topos(
        latitude_degrees=gs.latitude_deg,
        longitude_degrees=gs.longitude_deg,
        elevation_m=gs.altitude_m,
    )

    satellite = EarthSatellite(tle[1], tle[2], tle[0], ts)
    t, events = satellite.find_events(loc, t0, t1, gs.horizon_deg)

    observer = wgs84.latlon(gs.latitude_deg, gs.longitude_deg)
    diff = satellite - observer
    topocentric = diff.at(t)
    alt, az, _ = topocentric.altaz()

    # make a useful list of events
    i = 0
    passes = []
    for te, e in zip(t, events):
        if e == 0:  # AOS
            aos = te
            aos_i = i
        elif e == 1:  # culminated (there can be more than 1)
            cul = te
            cul_i = i
        elif e == 2:  # LOS
            los = te
            los_i = i
            try:
                passes.append([aos, cul, los, aos_i, cul_i, los_i])
            except Exception:
                pass  # don't add partial passes
        i += 1

    pass_list = []
    for aos, cul, los, aos_i, cul_i, los_i in passes:
        aos_utc = aos.utc_datetime()
        los_utc = los.utc_datetime()
        duration_s = (los_utc - aos_utc).total_seconds()
        max_el = alt.degrees[cul_i]
        aos_az = az.degrees[aos_i]
        los_az = az.degrees[los_i]

        if duration_s < min_duration_s or max_el < MIN_CUL_EL:
            continue

        pass_list.append(
            OrbitalPass(
                aos_utc=aos_utc.replace(tzinfo=None),
                los_utc=los_utc.replace(tzinfo=None),
                max_el=max_el,
                aos_az=aos_az,
                los_az=los_az,
            )
        )

    return pass_list
