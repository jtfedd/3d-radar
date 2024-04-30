from __future__ import annotations

import math
import os
from typing import Callable, List, Tuple, cast

import requests
import shapefile
import shapely
import shapely.geometry.base
from panda3d.core import LineSegs, NodePath, PandaNode, Vec3, Vec4

MAPS_FOLDER = "src/assets/maps/"

HOST = "https://www2.census.gov/geo/tiger/"

COUNTY_RAW = "TIGER2023/COUNTY/tl_2023_us_county.zip"
COUNTY_500K = "GENZ2022/shp/cb_2022_us_county_500k.zip"
COUNTY_5M = "GENZ2022/shp/cb_2022_us_county_5m.zip"
COUNTY_20M = "GENZ2022/shp/cb_2022_us_county_20m.zip"

STATE_RAW = "TIGER2023/STATE/tl_2023_us_state.zip"
STATE_500K = "GENZ2022/shp/cb_2022_us_state_500k.zip"
STATE_5M = "GENZ2022/shp/cb_2022_us_state_5m.zip"
STATE_20M = "GENZ2022/shp/cb_2022_us_state_20m.zip"

ROADS = "TIGER2023/PRISECROADS/tl_2023_{0:02d}_prisecroads.zip"

TOLERANCE_METERS = 250

EARTH_RADIUS = 6371000
EARTH_CIRCUMFERENCE = 2 * math.pi * EARTH_RADIUS
TOLERANCE = TOLERANCE_METERS / (EARTH_CIRCUMFERENCE / 360)


def collectLineStrings(
    linestrings: List[shapely.LineString],
    geometry: shapely.geometry.base.BaseGeometry,
) -> None:
    geomType = shapely.get_type_id(geometry)
    if geomType == shapely.GeometryType.LINESTRING:
        linestrings.append(geometry)
    if geomType == shapely.GeometryType.MULTILINESTRING:
        multiLineString = cast(shapely.MultiLineString, geometry)
        for linestring in multiLineString.geoms:
            linestrings.append(linestring)
    if geomType == shapely.GeometryType.GEOMETRYCOLLECTION:
        collection = cast(shapely.GeometryCollection, geometry)
        for geom in collection.geoms:
            collectLineStrings(linestrings, geom)


class Counter:
    def __init__(self) -> None:
        self.pointCount = 0
        self.lineStringCount = 0
        self.linearRingCount = 0
        self.polygonCount = 0
        self.multipointCount = 0
        self.multiLineStringCount = 0
        self.multiPolygonCount = 0
        self.geometryCollectionCount = 0

    def print(self) -> None:
        print("Geometry Counts:")
        print("  pointCount              ", self.pointCount)
        print("  lineStringCount         ", self.lineStringCount)
        print("  linearRingCount         ", self.linearRingCount)
        print("  polygonCount            ", self.polygonCount)
        print("  multipointCount         ", self.multipointCount)
        print("  multiLineStringCount    ", self.multiLineStringCount)
        print("  multiPolygonCount       ", self.multiPolygonCount)
        print("  geometryCollectionCounts", self.geometryCollectionCount)
        print("")


def countPoints(geometry: shapely.geometry.base.BaseGeometry, counter: Counter) -> None:
    geomType = shapely.get_type_id(geometry)
    if geomType == shapely.GeometryType.POINT:
        counter.pointCount += 1
    if geomType == shapely.GeometryType.LINESTRING:
        counter.lineStringCount += 1
        counter.pointCount += len(geometry.coords)
    if geomType == shapely.GeometryType.LINEARRING:
        counter.linearRingCount += 1
        counter.pointCount += len(geometry.coords)
    if geomType == shapely.GeometryType.POLYGON:
        counter.polygonCount += 1
        polygon = cast(shapely.Polygon, geometry)
        countPoints(polygon.exterior, counter)
        for ring in polygon.interiors:
            countPoints(ring, counter)
    if geomType == shapely.GeometryType.MULTIPOINT:
        counter.multipointCount += 1
        multipoint = cast(shapely.MultiPoint, geometry)
        for point in multipoint.geoms:
            countPoints(point, counter)
    if geomType == shapely.GeometryType.MULTILINESTRING:
        counter.multiLineStringCount += 1
        multiLineString = cast(shapely.MultiLineString, geometry)
        for linestring in multiLineString.geoms:
            countPoints(linestring, counter)
    if geomType == shapely.GeometryType.MULTIPOLYGON:
        counter.multiPolygonCount += 1
        multipolygon = cast(shapely.MultiPolygon, geometry)
        for polygon in multipolygon.geoms:
            countPoints(polygon, counter)
    if geomType == shapely.GeometryType.GEOMETRYCOLLECTION:
        counter.geometryCollectionCount += 1
        collection = cast(shapely.GeometryCollection, geometry)
        for geom in collection.geoms:
            countPoints(geom, counter)


def downloadAndMerge(files: List[str]) -> shapely.geometry.base.BaseGeometry:
    shapes = []

    for f in files:
        filename = HOST + f
        print("Downloading", filename)
        r = requests.head(filename, allow_redirects=True, timeout=10)
        if r.status_code == 404:
            print("Does not exist")
            continue

        shape = shapely.geometry.shape(shapefile.Reader(filename).shapes())
        shapes.append(shape)

    return shapely.geometry.GeometryCollection(shapes)


def loadStates() -> shapely.geometry.base.BaseGeometry:
    return downloadAndMerge([STATE_500K])


def loadCounties() -> shapely.geometry.base.BaseGeometry:
    return downloadAndMerge([COUNTY_500K])


def loadRoads() -> shapely.geometry.base.BaseGeometry:
    return downloadAndMerge([ROADS.format(i) for i in range(80)])


def openOrCreate(
    filename: str,
    create: Callable[[], shapely.geometry.base.BaseGeometry],
) -> shapely.geometry.base.BaseGeometry:
    filepath = MAPS_FOLDER + filename + ".json"
    if os.path.exists(filepath):
        print("Checking", filepath, "- exists")
        with open(filepath, "r", encoding="utf-8") as f:
            print("Reading", filepath)
            fileJson = f.read()
            return shapely.from_geojson(fileJson)

    print("Checking", filepath, "- does not exist")
    shape = create()
    with open(filepath, "w", encoding="utf-8") as f:
        print("Writing", filepath)
        f.write(shapely.to_geojson(shape))

    return shape


def writeBam(node: NodePath[PandaNode], filename: str) -> None:
    filepath = MAPS_FOLDER + filename + ".bam"
    print("Writing", filepath)
    node.writeBamFile(filepath)


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


def toGlobe(coord: Tuple[float, float]) -> Vec3:
    az = math.radians(coord[0])
    el = math.radians(coord[1])

    x = math.cos(az) * math.cos(el)
    y = math.sin(az) * math.cos(el)
    z = math.sin(el)

    return Vec3(x, y, z)


def drawSegs(seq: shapely.geometry.base.CoordinateSequence, lineSegs: LineSegs) -> None:
    coords = list(seq)

    lineSegs.moveTo(toGlobe(coords[0]))

    for point in coords:
        lineSegs.drawTo(toGlobe(point))


def draw(geometry: shapely.geometry.base.BaseGeometry, lineSegs: LineSegs) -> None:
    geomType = shapely.get_type_id(geometry)

    if geomType == shapely.GeometryType.LINESTRING:
        drawSegs(geometry.coords, lineSegs)
    if geomType == shapely.GeometryType.LINEARRING:
        drawSegs(geometry.coords, lineSegs)
    if geomType == shapely.GeometryType.POLYGON:
        polygon = cast(shapely.Polygon, geometry)
        draw(polygon.exterior, lineSegs)
        for ring in polygon.interiors:
            draw(ring, lineSegs)
    if geomType == shapely.GeometryType.MULTILINESTRING:
        multiLineString = cast(shapely.MultiLineString, geometry)
        for linestring in multiLineString.geoms:
            draw(linestring, lineSegs)
    if geomType == shapely.GeometryType.MULTIPOLYGON:
        multipolygon = cast(shapely.MultiPolygon, geometry)
        for polygon in multipolygon.geoms:
            draw(polygon, lineSegs)
    if geomType == shapely.GeometryType.GEOMETRYCOLLECTION:
        collection = cast(shapely.GeometryCollection, geometry)
        for geom in collection.geoms:
            draw(geom, lineSegs)


def render(
    geometry: shapely.geometry.base.BaseGeometry,
    thickness: float,
    filename: str,
) -> None:
    print("Rendering", filename)
    lineSegs = LineSegs()
    lineSegs.setColor(Vec4(1, 1, 1, 1))
    lineSegs.setThickness(thickness)
    draw(geometry, lineSegs)

    writeBam(NodePath(lineSegs.create()), filename)


if __name__ == "__main__":
    render(openOrCreate("states", loadStates), 2, "states")
    render(openOrCreate("counties", loadCounties), 1, "counties")
    render(openOrCreate("roads_simple", simplfyRoads), 1, "roads")
