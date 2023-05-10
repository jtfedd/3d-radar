from direct.showbase.ShowBase import ShowBase

from lib.geometry import mesh_sharp
from lib.geometry import mesh_smooth

import numpy as np
import mcubes

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

        # Extract the 0-isosurface
        vertices, triangles = mcubes.marching_cubes(u, 0)

        # The vertices that come from marching cubes are "wound" the wrong way, causing
        # the faces to all be facing inward instead of outward.
        # If we swap columns 1 and 2, leaving column 0 in place, this reverses the order
        # and causes the faces to be "wound" the correct way. This makes the rest of
        # the code a little less confusing.
        triangles[:, [1, 2]] = triangles[:, [2, 1]]

        geomNode = mesh_smooth.trianglesToGeometry(vertices, triangles)
        nodePath = self.render.attachNewNode(geomNode)

        # Render a cube for comparison
        cube = self.loader.loadModel("../assets/cube.glb")
        cube.reparentTo(self.render)


app = App()
app.run()
