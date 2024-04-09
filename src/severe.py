import concurrent.futures
import math
from typing import List, Tuple

import requests
from direct.showbase.ShowBase import ShowBase
from panda3d.core import LineSegs, NodePath, Vec3, Vec4

SEVERE_URL = "https://api.weather.gov/alerts/active"
params = {
    "status": "actual",
    "limit": 500,
}


def getZoneGeometry(zoneUrl: str) -> str:
    rq = requests.get(zoneUrl, timeout=10)
    rqj = rq.json()
    return rqj["geometry"]


def toGlobe(coord: Tuple[float, float]) -> Vec3:
    az = math.radians(coord[0])
    el = math.radians(coord[1])

    x = math.cos(az) * math.cos(el)
    y = math.sin(az) * math.cos(el)
    z = math.sin(el)

    return Vec3(x, y, z)


def drawSegs(seq: List[Tuple[float, float]], lineSegs: LineSegs) -> None:
    print("drawing", len(seq))

    lineSegs.moveTo(toGlobe(seq[0]))

    for point in seq:
        lineSegs.drawTo(toGlobe(point))


def getGeoms(code: str) -> List[List[Tuple[float, float]]]:
    p = params.copy()
    p["code"] = code
    r = requests.get(SEVERE_URL, params=p, timeout=10)
    responseJson = r.json()

    features = responseJson["features"]

    g = []
    zones = []

    print(len(features))
    for f in features:
        print(f["properties"]["event"])
        geometry = f["geometry"]

        if geometry is None:
            affectedZones = f["properties"]["affectedZones"]
            print(affectedZones)
            for zone in affectedZones:
                zones.append(zone)
        else:
            print(geometry)
            g.append(geometry["coordinates"][0])

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(getZoneGeometry, zone) for zone in zones}
        for future in concurrent.futures.as_completed(futures):
            zoneGeometry = future.result()
            print(
                zoneGeometry["type"],
                len(zoneGeometry["coordinates"], len(zoneGeometry["coordinates"][0])),
            )
            g.append(zoneGeometry["coordinates"][0])

    return g


base = ShowBase()
root = base.render.attachNewNode("root")
root.setScale(100)
wroot = base.render.attachNewNode("wroot")
wroot.setScale(100.001)


def addAlert(code: str, color: Vec4) -> None:
    print("alert", code, color)
    lineSegs = LineSegs()
    lineSegs.setColor(color)
    lineSegs.setThickness(2)

    geoms = getGeoms(code)
    for geo in geoms:
        drawSegs(geo, lineSegs)
    print("finished drawing")

    a = NodePath(lineSegs.create())
    a.reparentTo(wroot)
    print("finished rendering")


states = base.loader.loadModel("assets/maps/states.bam")
states.reparentTo(root)

counties = base.loader.loadModel("assets/maps/counties.bam")
counties.reparentTo(root)

colors = {
    "TOW": Vec4(1, 0, 0, 1),
    "TOA": Vec4(1, 0, 0, 1),
    "SVW": Vec4(1, 1, 0, 1),
    "SVA": Vec4(1, 1, 0, 1),
    "WWY": Vec4(1, 0, 1, 1),
}

with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = {
        executor.submit(addAlert, code, colors[code])
        # for code in ["TOW", "TOA", "SVW", "SVA"]
        for code in ["TOW", "SVW"]
        # for code in ["WWY"]
    }
    for future in concurrent.futures.as_completed(futures):
        pass


base.run()
