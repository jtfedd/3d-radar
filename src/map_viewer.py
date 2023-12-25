from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec4

from lib.app.context import AppContext
from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.camera.camera_control import CameraControl
from lib.ui.core.colors import UIColors


class App:
    def __init__(self, base: ShowBase) -> None:
        base.setBackgroundColor(0, 0, 0, 1)

        self.state = AppState()
        self.events = AppEvents()
        self.ctx = AppContext(base, self.events, self.state)
        self.cameraControl = CameraControl(self.ctx, self.events)

        self.states = MapLayer(base, "states", UIColors.MAP_BOUNDARIES)
        self.counties = MapLayer(base, "counties", UIColors.MAP_BOUNDARIES)
        self.roads = MapLayer(base, "roads", UIColors.MAP_DETAILS)


class MapLayer:
    def __init__(self, base: ShowBase, layer: str, color: Vec4) -> None:
        self.node = base.loader.loadModel("assets/maps/" + layer + ".bam")
        if self.node:
            self.node.reparentTo(base.render)
            self.node.setScale(1000)
            self.node.setColorScale(color)


b = ShowBase()
a = App(b)
b.run()
