from panda3d.core import Point2

from lib.model.geo_point import GeoPoint


class ContextMenuPayload:
    def __init__(self, screenPoint: Point2, geoPoint: GeoPoint):
        self.screenPoint = screenPoint
        self.geoPoint = geoPoint
