from __future__ import annotations

import math

from panda3d.core import NodePath, PandaNode

from lib.app.state import AppState
from lib.geometry.circle import drawCircle
from lib.ui.core.colors import UIColors
from lib.ui.core.layers import UILayer
from lib.util.events.listener import Listener


class LatLonLines(Listener):
    def __init__(self, state: AppState, root: NodePath[PandaNode]) -> None:
        super().__init__()

        self.root = root.attachNewNode("map-lat-lon-lines")
        self.root.setColorScale(UIColors.MAP_LAT_LON)
        self.root.setBin("background", UILayer.MAP_LAT_LON.value)

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

        self.bind(
            state.mapLatLon,
            lambda visible: self.root.show() if visible else self.root.hide(),
        )
