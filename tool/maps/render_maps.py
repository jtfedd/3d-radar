import math
from typing import Tuple, cast

import shapely
import shapely.geometry.base
from file_util import writeBam
from panda3d.core import LineSegs, NodePath, Vec3, Vec4


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
