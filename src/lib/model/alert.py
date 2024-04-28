from typing import List

from .alert_type import AlertType
from .geo_point import GeoPoint


class Alert:
    def __init__(self, alertType: AlertType, name: str, boundary: List[List[GeoPoint]]):
        self.alertType = alertType
        self.name = name
        self.boundary = boundary

    def center(self) -> GeoPoint:
        minLat = 1000.0
        maxLat = -1000.0
        minLon = 1000.0
        maxLon = -1000.0

        for ring in self.boundary:
            for point in ring:
                minLat = min(minLat, point.lat)
                maxLat = max(maxLat, point.lat)
                minLon = min(minLon, point.lon)
                maxLon = max(maxLon, point.lon)

        return GeoPoint((minLat + maxLat) / 2, (minLon + maxLon) / 2)
