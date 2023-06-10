import timeit

import numpy as np
import perlin_numpy
from direct.showbase.ShowBase import ShowBase
from panda3d.core import AmbientLight, DirectionalLight

from lib.geometry import marching_cubes, triangles_to_geometry


class App(ShowBase):
    def __init__(self) -> None:
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
        x, y, z = np.mgrid[:30, :30, :30]
        u = (x - 15) ** 2 + (y - 15) ** 2 + (z - 15) ** 2 - 8**2
        u = u.astype(dtype=float)

        # Generate some noise
        noise = perlin_numpy.generate_perlin_noise_3d(u.shape, (6, 6, 6))
        u += noise * 75

        num = 100

        vertices, triangles = marching_cubes.getIsosurface(u, 0)

        print(
            "Sharp",
            timeit.timeit(
                lambda: triangles_to_geometry.getGeometry(
                    vertices, triangles, smooth=False
                ),
                number=num,
            )
            / num,
        )

        print(
            "Smooth",
            timeit.timeit(
                lambda: triangles_to_geometry.getGeometry(
                    vertices, triangles, smooth=True
                ),
                number=num,
            )
            / num,
        )

        sharpGeom = triangles_to_geometry.getGeometry(vertices, triangles, smooth=False)
        sharpNode = self.render.attachNewNode(sharpGeom)
        sharpNode.setZ(-15)

        smoothGeom = triangles_to_geometry.getGeometry(vertices, triangles, smooth=True)
        smoothNode = self.render.attachNewNode(smoothGeom)
        smoothNode.setX(30)
        smoothNode.setZ(-15)

        # Render a cube for comparison
        cube = self.loader.loadModel("../assets/cube.glb")
        if cube:
            cube.reparentTo(self.render)


app = App()
app.run()
