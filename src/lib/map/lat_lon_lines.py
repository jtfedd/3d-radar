from __future__ import annotations

import math

from panda3d.core import NodePath, PandaNode

from lib.geometry.circle import drawCircle
from lib.ui.core.colors import UIColors


class LatLonLines:
    def __init__(self, root: NodePath[PandaNode]) -> None:
        self.root = root.attachNewNode("map-lat-lon-lines")
        self.root.setColorScale(UIColors.MAP_LAT_LON)

        for i in range(-8, 9):
            lat = 10 * i
            circle = self.root.attachNewNode(drawCircle())
            circle.setScale(math.cos(math.radians(lat)))
            circle.setZ(math.sin(math.radians(lat)))

        for i in range(0, 18):
            lon = 10 * i
            circle = self.root.attachNewNode(drawCircle())
            circle.setP(90)
            circle.setH(lon)
