import math
from typing import List

import shapely
import shapely.geometry.base
from download_maps import loadRoads
from file_util import openOrCreate
from shape_util import Counter, collectLineStrings, countPoints

TOLERANCE_METERS = 250

EARTH_RADIUS = 6378100
EARTH_CIRCUMFERENCE = 2 * math.pi * EARTH_RADIUS
TOLERANCE = TOLERANCE_METERS / (EARTH_CIRCUMFERENCE / 360)


def mergeRoads() -> shapely.geometry.base.BaseGeometry:
    raw = openOrCreate("roads_raw", loadRoads)

    print("Collecting Lines")
    linestrings: List[shapely.LineString] = []
    collectLineStrings(linestrings, raw)
    print("LineStrings:", len(linestrings))

    print("Performing Union")
    union = shapely.union_all(linestrings)

    print("Performing Merge")
    merged = shapely.line_merge(union)

    mergedCounter = Counter()
    countPoints(merged, mergedCounter)
    mergedCounter.print()

    return merged


def simplfyRoads() -> shapely.geometry.base.BaseGeometry:
    merged = openOrCreate("roads_merged", mergeRoads)

    print("Simplifying Roads")
    print("Tolerance:", str(TOLERANCE_METERS) + "m", TOLERANCE)

    simplified = shapely.simplify(merged, TOLERANCE, preserve_topology=False)

    simple = Counter()
    countPoints(simplified, simple)
    simple.print()

    return simplified
