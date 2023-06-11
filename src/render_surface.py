import numpy as np
from direct.showbase.ShowBase import ShowBase

from lib.camera.camera_control import CameraControl
from lib.geometry import marching_cubes, reshape, triangles_to_geometry
from lib.util.util import defaultLight, getData


class Viewer(ShowBase):
    def __init__(self) -> None:
        ShowBase.__init__(self)
        self.setBackgroundColor(0, 0, 0, 1)
        defaultLight(self)

        self.cameraControl = CameraControl(self)

        scan = getData()

        data = scan.reflectivity
        data = np.isnan(data)

        vertices, triangles = marching_cubes.getIsosurface(data, 0.5)
        vertices = reshape.reshape(vertices, scan)

        geom = triangles_to_geometry.getGeometry(vertices, triangles, smooth=False)
        self.render.attachNewNode(geom)

        print("Done!")


app = Viewer()
app.run()
