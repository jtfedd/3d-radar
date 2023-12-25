from __future__ import annotations

import os
from typing import Callable

import shapely
import shapely.geometry.base
from panda3d.core import NodePath, PandaNode

MAPS_FOLDER = "src/assets/maps/"


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
