from typing import List, cast

import shapely.geometry
import shapely.geometry.base


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
