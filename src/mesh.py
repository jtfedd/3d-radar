from direct.showbase.ShowBase import ShowBase

from lib.geometry import mesh_sharp
from lib.geometry import mesh_smooth
from lib.geometry import marching_cubes
from lib.camera.camera_control import CameraControl

import numpy as np
import perlin_numpy

import timeit

from panda3d.core import DirectionalLight, AmbientLight


class App(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Make some light
        dlight = DirectionalLight("dlight")
        dlight.setColor((0.8, 0.8, 0.5, 1))
        dlnp = self.render.attachNewNode(dlight)
        dlnp.setHpr(0, -60, 0)
        self.render.setLight(dlnp)

        alight = AmbientLight("alight")
        alight.setColor((0.2, 0.2, 0.2, 1))
        alnp = self.render.attachNewNode(alight)
        self.render.setLight(alnp)

        # Create a data volume (30 x 30 x 30)
        X, Y, Z = np.mgrid[:30, :30, :30]
        u = (X - 15) ** 2 + (Y - 15) ** 2 + (Z - 15) ** 2 - 8**2
        u = u.astype(dtype=float)

        # Generate some noise
        noise = perlin_numpy.generate_perlin_noise_3d(u.shape, (6, 6, 6))
        u += noise * 75

        # Extract the 0-isosurface
        vertices, triangles = marching_cubes.getIsosurface(u, 0)

        print(
            timeit.timeit(
                lambda: mesh_sharp.trianglesToGeometry(vertices, triangles), number=100
            )
        )

        print(
            timeit.timeit(
                lambda: mesh_smooth.trianglesToGeometry(vertices, triangles), number=100
            )
        )

        sharp_geom = mesh_sharp.trianglesToGeometry(vertices, triangles)
        sharp_node = self.render.attachNewNode(sharp_geom)
        sharp_node.setZ(-15)

        smooth_geom = mesh_smooth.trianglesToGeometry(vertices, triangles)
        smooth_node = self.render.attachNewNode(smooth_geom)
        smooth_node.setX(30)
        smooth_node.setZ(-15)

        # Render a cube for comparison
        cube = self.loader.loadModel("../assets/cube.glb")
        cube.reparentTo(self.render)


app = App()
app.run()
