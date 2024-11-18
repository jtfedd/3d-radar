from __future__ import annotations

import math

from panda3d.core import Point3, Vec3

from lib.app.context import AppContext
from lib.map.constants import EARTH_RADIUS
from lib.model.geo_point import GeoPoint
from lib.util.map_3d_to_2d import map3dToAspect2d


def toGlobe(point: GeoPoint) -> Vec3:
    """Returns a unit vector pointing toward the given GeoPoint
    on the surface of the globe"""

    az = math.radians(point.lon)
    el = math.radians(point.lat)

    x = math.cos(az) * math.cos(el)
    y = math.sin(az) * math.cos(el)
    z = math.sin(el)

    return Vec3(x, y, z)


def toScreen(ctx: AppContext, point: Point3) -> Point3 | None:
    worldCenter = Vec3(0, 0, -EARTH_RADIUS)
    worldToPoint = point - worldCenter
    cameraToPoint = point - ctx.base.camera.getPos(ctx.base.render)
    if cameraToPoint.dot(worldToPoint) > 0:
        return None

    return map3dToAspect2d(ctx, point)
