import math
from typing import Self

from lib.map.constants import EARTH_RADIUS


class GeoPoint:
    def __init__(self, lat: float, lon: float):
        self.lat = lat
        self.lon = lon

    def __hash__(self) -> int:
        return hash((self.lat, self.lon))

    def dist(self, other: Self) -> float:
        lat1 = math.radians(self.lat)
        lat2 = math.radians(other.lat)

        dLat = math.radians(other.lat - self.lat)
        dLon = math.radians(other.lon - self.lon)

        # apply formulae
        a = pow(
            math.sin(dLat / 2),
            2,
        ) + pow(
            math.sin(dLon / 2),
            2,
        ) * math.cos(
            lat1
        ) * math.cos(lat2)
        c = 2 * math.asin(math.sqrt(a))

        return EARTH_RADIUS * c
