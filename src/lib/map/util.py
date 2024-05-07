from __future__ import annotations

import math

from panda3d.core import Vec3

from lib.model.geo_point import GeoPoint


def toGlobe(point: GeoPoint) -> Vec3:
    """Returns a unit vector pointing toward the given GeoPoint
    on the surface of the globe"""

    az = math.radians(point.lon)
    el = math.radians(point.lat)

    x = math.cos(az) * math.cos(el)
    y = math.sin(az) * math.cos(el)
    z = math.sin(el)

    return Vec3(x, y, z)
