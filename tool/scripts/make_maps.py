from __future__ import annotations

import math
import os
import pathlib
from typing import Callable, List, Tuple, cast

import requests
import shapefile
import shapely
import shapely.geometry.base
from panda3d.core import (
    Geom,
    GeomLinestripsAdjacency,
    GeomNode,
    GeomVertexData,
    GeomVertexFormat,
    GeomVertexWriter,
    NodePath,
    PandaNode,
    Vec3,
)
from shapely.coords import CoordinateSequence

MAPS_FOLDER = "src/assets/maps/"
MAPS_CACHE_FOLDER = MAPS_FOLDER + "cache/"
MAPS_SOURCE_YEAR = "2024"

HOST = "https://www2.census.gov/geo/tiger/"
REQUESTS_TIMEOUT = 60  # Note: census.gov server has been squirrelly lately

COUNTY_RAW = f"TIGER{MAPS_SOURCE_YEAR}/COUNTY/tl_{MAPS_SOURCE_YEAR}_us_county.zip"
COUNTY_500K = f"GENZ{MAPS_SOURCE_YEAR}/shp/cb_{MAPS_SOURCE_YEAR}_us_county_500k.zip"
COUNTY_5M = f"GENZ{MAPS_SOURCE_YEAR}/shp/cb_{MAPS_SOURCE_YEAR}_us_county_5m.zip"
COUNTY_20M = f"GENZ{MAPS_SOURCE_YEAR}/shp/cb_{MAPS_SOURCE_YEAR}_us_county_20m.zip"

STATE_RAW = f"TIGER{MAPS_SOURCE_YEAR}/STATE/tl_{MAPS_SOURCE_YEAR}_us_state.zip"
STATE_500K = f"GENZ{MAPS_SOURCE_YEAR}/shp/cb_{MAPS_SOURCE_YEAR}_us_state_500k.zip"
STATE_5M = f"GENZ{MAPS_SOURCE_YEAR}/shp/cb_{MAPS_SOURCE_YEAR}_us_state_5m.zip"
STATE_20M = f"GENZ{MAPS_SOURCE_YEAR}/shp/cb_{MAPS_SOURCE_YEAR}_us_state_20m.zip"

ROADS = (
    f"TIGER{MAPS_SOURCE_YEAR}/PRISECROADS/"
    f"tl_{MAPS_SOURCE_YEAR}_{{0:02d}}_prisecroads.zip"
)

TOLERANCE_METERS = 250

EARTH_RADIUS = 6371000
EARTH_CIRCUMFERENCE = 2 * math.pi * EARTH_RADIUS
TOLERANCE = TOLERANCE_METERS / (EARTH_CIRCUMFERENCE / 360)


def collectLineStrings(
    linestrings: List[shapely.LineString],
    geometry: shapely.geometry.base.BaseGeometry,
) -> None:
    if isinstance(geometry, shapely.LineString):
        linestrings.append(geometry)
    elif isinstance(geometry, shapely.MultiLineString):
        for linestring in geometry.geoms:
            linestrings.append(linestring)
    elif isinstance(geometry, shapely.GeometryCollection):
        for geom in geometry.geoms:
            collectLineStrings(linestrings, geom)
    else:
        # Optionally, log or raise for unsupported geometry types
        raise TypeError(
            f"Warning: Unsupported geometry type: {type(geometry).__name__}"
        )


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

    # Set up cache directory
    cacheRoot = pathlib.Path(MAPS_CACHE_FOLDER)
    cacheRoot.mkdir(parents=True, exist_ok=True)

    for f in files:
        # Use the file path as a subpath in the cache
        cachePath = cacheRoot / f
        cachePath.parent.mkdir(parents=True, exist_ok=True)

        if cachePath.exists():
            print(f"Using cached file: {cachePath}")
            shapeReader = shapefile.Reader(str(cachePath))
        else:
            filename = HOST + f
            print("Downloading", filename)
            r = requests.get(filename, allow_redirects=True, timeout=REQUESTS_TIMEOUT)
            if r.status_code == 404:
                print("...but it does not exist")
                continue
            # Save to cache
            with open(cachePath, "wb") as out:
                out.write(r.content)
            print(f"Saved to cache: {cachePath}")
            shapeReader = shapefile.Reader(str(cachePath))

        shape = shapely.geometry.shape(
            shapeReader.shapes(),  # type:ignore[unused-ignore]
        )
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
    forceDownload: bool = False,
) -> shapely.geometry.base.BaseGeometry:
    filepath = MAPS_FOLDER + filename + ".json"
    if os.path.exists(filepath):
        if not forceDownload:
            print("Checking", filepath, "- exists")
            with open(filepath, "r", encoding="utf-8") as f:
                print("Reading", filepath)
                fileJson = f.read()
                return shapely.from_geojson(fileJson)
        else:
            print(
                (
                    f"File {filepath} exists, but will be re-created "
                    "from a new download (force update enabled)"
                )
            )
    else:
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


def mergeRoads(forceDownload: bool = False) -> shapely.geometry.base.BaseGeometry:
    raw = openOrCreate(
        "roads_raw",
        loadRoads,
        forceDownload=forceDownload,
    )

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


def simplfyRoads(forceDownload: bool = False) -> shapely.geometry.base.BaseGeometry:
    merged = openOrCreate(
        "roads_merged",
        lambda: mergeRoads(forceDownload=forceDownload),
        forceDownload=forceDownload,
    )

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


class LineDrawer:
    def __init__(self) -> None:
        self.infos: List[LinesAdjacencyInfo] = []

    def add(self, info: LinesAdjacencyInfo) -> None:
        self.infos.append(info)

    def create(self) -> NodePath[PandaNode]:
        vertexCount = sum(info.count() for info in self.infos)

        vdata = GeomVertexData("name", GeomVertexFormat.getV3(), Geom.UHStatic)
        vdata.setNumRows(vertexCount)

        vertex = GeomVertexWriter(vdata, "vertex")
        prim = GeomLinestripsAdjacency(Geom.UH_static)

        index = 0
        for info in self.infos:
            points = info.getPoints()
            if len(points) < 2:
                continue

            firstIndex = index
            lastIndex = index + len(points) - 1
            index += len(points)

            for point in points:
                vertex.addData3(point)

            # Leading control point
            if info.isLoop:
                prim.addVertex(lastIndex)
            else:
                prim.addVertex(firstIndex + 1)

            for i in range(firstIndex, lastIndex + 1):
                prim.addVertex(i)

            # Trailing control point
            if info.isLoop:
                prim.addVertex(firstIndex)
                prim.addVertex(firstIndex + 1)
            else:
                prim.addVertex(lastIndex - 1)

            prim.closePrimitive()

        geom = Geom(vdata)
        geom.addPrimitive(prim)

        node = GeomNode("gnode")
        node.addGeom(geom)

        return NodePath(node)


class LinesAdjacencyInfo:
    def __init__(self) -> None:
        self.isLoop = False
        self.points: List[Vec3] = []

    def add(self, point: Vec3) -> None:
        self.points.append(point)
        self.isLoop = self.points[0] == point

    def count(self) -> int:
        if self.isLoop:
            return len(self.points) - 1
        return len(self.points)

    def getPoints(self) -> List[Vec3]:
        if self.isLoop:
            return self.points[:-1]
        return self.points


def drawSegs(seq: CoordinateSequence, drawer: LineDrawer) -> None:
    coords = list(seq)

    info = LinesAdjacencyInfo()
    for point in coords:
        assert len(point) == 2
        info.add(toGlobe(point))

    drawer.add(info)


def draw(geometry: shapely.geometry.base.BaseGeometry, drawer: LineDrawer) -> None:
    geomType = shapely.get_type_id(geometry)

    if geomType == shapely.GeometryType.LINESTRING:
        drawSegs(geometry.coords, drawer)
    if geomType == shapely.GeometryType.LINEARRING:
        drawSegs(geometry.coords, drawer)
    if geomType == shapely.GeometryType.POLYGON:
        polygon = cast(shapely.Polygon, geometry)
        draw(polygon.exterior, drawer)
        for ring in polygon.interiors:
            draw(ring, drawer)
    if geomType == shapely.GeometryType.MULTILINESTRING:
        multiLineString = cast(shapely.MultiLineString, geometry)
        for linestring in multiLineString.geoms:
            draw(linestring, drawer)
    if geomType == shapely.GeometryType.MULTIPOLYGON:
        multipolygon = cast(shapely.MultiPolygon, geometry)
        for polygon in multipolygon.geoms:
            draw(polygon, drawer)
    if geomType == shapely.GeometryType.GEOMETRYCOLLECTION:
        collection = cast(shapely.GeometryCollection, geometry)
        for geom in collection.geoms:
            draw(geom, drawer)


def render(
    geometry: shapely.geometry.base.BaseGeometry,
    filename: str,
) -> None:
    print("Rendering", filename)

    drawer = LineDrawer()
    draw(geometry, drawer)

    writeBam(drawer.create(), filename)


if __name__ == "__main__":
    answer = (
        input(
            "Attempt to download updates even if geometry files already exist? [y/N]: "
        )
        .strip()
        .lower()
    )
    shouldForceDownload = answer == "y"

    render(
        openOrCreate(
            "states",
            loadStates,
            forceDownload=shouldForceDownload,
        ),
        "states",
    )
    render(
        openOrCreate(
            "counties",
            loadCounties,
            forceDownload=shouldForceDownload,
        ),
        "counties",
    )
    render(
        openOrCreate(
            "roads_simple",
            lambda: simplfyRoads(forceDownload=shouldForceDownload),
            forceDownload=shouldForceDownload,
        ),
        "roads",
    )
