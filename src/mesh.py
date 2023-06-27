import timeit

import numpy as np
import numpy.typing as npt
import perlin_numpy
from direct.showbase.ShowBase import ShowBase

from lib.geometry import marching_cubes, triangles_to_geometry
from lib.util.util import defaultLight


class App(ShowBase):
    TIMING_ITERATIONS = 100

    def __init__(self) -> None:
        ShowBase.__init__(self)
        defaultLight(self)

        u = self.makeData()

        # Generate some noise
        noise = perlin_numpy.generate_perlin_noise_3d(u.shape, (6, 6, 6))
        u += noise * 75

        vertices, triangles = marching_cubes.getIsosurface(u, 0)

        self.doTiming(vertices, triangles)

        sharpGeom = triangles_to_geometry.getGeometry(vertices, triangles, smooth=False)
        sharpNode = self.render.attachNewNode(sharpGeom)
        sharpNode.setZ(-15)

        smoothGeom = triangles_to_geometry.getGeometry(vertices, triangles, smooth=True)
        smoothNode = self.render.attachNewNode(smoothGeom)
        smoothNode.setX(30)
        smoothNode.setZ(-15)

        # Render a cube for comparison
        cube = self.loader.loadModel("assets/cube.glb")
        if cube:
            cube.reparentTo(self.render)

    def makeData(self) -> npt.NDArray[np.float32]:
        # Create a data volume (30 x 30 x 30)
        x, y, z = np.mgrid[:30, :30, :30]
        u: npt.NDArray[np.float32] = (
            (x - 15) ** 2 + (y - 15) ** 2 + (z - 15) ** 2 - 8**2
        ).astype(np.float32)
        return u

    def doTiming(
        self, vertices: npt.NDArray[np.float32], triangles: npt.NDArray[np.uint32]
    ) -> None:
        print(
            "Sharp",
            timeit.timeit(
                lambda: triangles_to_geometry.getGeometry(
                    vertices, triangles, smooth=False
                ),
                number=self.TIMING_ITERATIONS,
            )
            / self.TIMING_ITERATIONS,
        )

        print(
            "Smooth",
            timeit.timeit(
                lambda: triangles_to_geometry.getGeometry(
                    vertices, triangles, smooth=True
                ),
                number=self.TIMING_ITERATIONS,
            )
            / self.TIMING_ITERATIONS,
        )


app = App()
app.run()
