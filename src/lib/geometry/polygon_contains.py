from typing import List

from lib.model.geo_point import GeoPoint


def polygonContains(ring: List[GeoPoint], p: GeoPoint) -> bool:
    contains = False

    i = 0
    j = len(ring) - 1

    testX = p.lon
    testY = p.lat

    while i < len(ring):
        vertIX = ring[i].lon
        vertIY = ring[i].lat

        vertJX = ring[j].lon
        vertJY = ring[j].lat

        if ((vertIY > testY) != (vertJY > testY)) and (
            testX < (vertJX - vertIX) * (testY - vertIY) / (vertJY - vertIY) + vertIX
        ):
            contains = not contains

        j = i
        i += 1

    return contains
