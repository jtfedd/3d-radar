import numpy as np
import numpy.typing as npt
from direct.showbase.ShowBase import ShowBase
from panda3d.core import TransparencyAttrib

from lib.app.context import AppContext
from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.camera.camera_control import CameraControl
from lib.geometry import marching_cubes, reshape, triangles_to_geometry
from lib.model.scan import Scan
from lib.util.util import defaultLight, getData


class Viewer:
    def __init__(self, base: ShowBase) -> None:
        self.base = base
        base.setBackgroundColor(0, 0, 0, 1)
        defaultLight(base)

        events = AppEvents()
        state = AppState()
        self.cameraControl = CameraControl(AppContext(base, events, state), events)
        base.accept("w", base.toggle_wireframe)

        scan = getData()

        data = scan.reflectivity

        booleanData = np.isnan(data)
        vertices, triangles = marching_cubes.getIsosurface(booleanData, 0.5)
        vertices = reshape.reshape(vertices, scan)
        geom = triangles_to_geometry.getGeometry(vertices, triangles, smooth=False)
        node = base.render.attachNewNode(geom)
        node.setTransparency(TransparencyAttrib.MAlpha)
        node.setColorScale(1, 1, 1, 0.1)
        node.setLightOff()
        node.setBin("fixed", 5)

        minValue = np.nanmin(data)
        data = np.nan_to_num(data, nan=float(minValue))
        data = np.negative(data)

        self.addIso(data, scan, 4, 5, 0, 0, 1, 0.1)
        self.addIso(data, scan, 3, -10, 0, 1, 0, 0.1)
        self.addIso(data, scan, 2, -35, 1, 1, 0, 0.1)
        self.addIso(data, scan, 1, -45, 1, 0.5, 0, 0.1)
        self.addIso(data, scan, 0, -55, 1, 0, 0, 0.1)

        print("Done!")

    def addIso(
        self,
        data: npt.NDArray[np.float32],
        scan: Scan,
        renderBin: int,
        level: float,
        red: float,
        green: float,
        blue: float,
        alpha: float,
    ) -> None:
        print("Iso", level)

        vertices, triangles = marching_cubes.getIsosurface(data, level)
        vertices = reshape.reshape(vertices, scan)
        geom = triangles_to_geometry.getGeometry(vertices, triangles, smooth=False)

        node = self.base.render.attachNewNode(geom)
        node.setTransparency(TransparencyAttrib.MAlpha)
        node.setColorScale(red, green, blue, alpha)
        node.setLightOff()
        node.setBin("fixed", renderBin)


b = ShowBase()
app = Viewer(b)
b.run()
