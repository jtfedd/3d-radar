import numpy as np
import numpy.typing as npt
from direct.showbase.ShowBase import ShowBase
from panda3d.core import TransparencyAttrib

from lib.camera.camera_control import CameraControl
from lib.geometry import marching_cubes, reshape, triangles_to_geometry
from lib.model.scan import Scan
from lib.util.util import defaultLight, getData


class Viewer(ShowBase):
    def __init__(self) -> None:
        ShowBase.__init__(self)
        self.setBackgroundColor(0, 0, 0, 1)
        defaultLight(self)

        self.cameraControl = CameraControl(self)
        self.accept("w", self.toggle_wireframe)

        self.radarBase = self.render.attachNewNode("radar")

        scan = getData()

        data = scan.reflectivity

        booleanData = np.isnan(data)
        vertices, triangles = marching_cubes.getIsosurface(booleanData, 0.5)
        vertices = reshape.reshape(vertices, scan)
        geom = triangles_to_geometry.getGeometry(vertices, triangles, smooth=False)
        node = self.render.attachNewNode(geom)
        node.setTransparency(TransparencyAttrib.MAlpha)
        node.setColorScale(1, 1, 1, 0.1)

        print("Done!")

    def addIso(
        self,
        data: npt.NDArray[np.float32],
        scan: Scan,
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

        node = self.render.attachNewNode(geom)
        node.setTransparency(TransparencyAttrib.MAlpha)
        node.setColorScale(red, green, blue, alpha)


app = Viewer()
app.run()
