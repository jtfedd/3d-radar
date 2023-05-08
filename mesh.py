from direct.showbase.ShowBase import ShowBase

import numpy as np
import mcubes

from panda3d.core import (
    GeomVertexData,
    GeomVertexFormat,
    GeomVertexWriter,
    GeomTriangles,
    GeomNode,
    Geom,
)

from panda3d.core import DirectionalLight, AmbientLight, TransparencyAttrib


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

        # unique_vertices, vertex_mapping = np.unique(
        #     vertices, axis=0, return_inverse=True
        # )

        vdata = GeomVertexData("name", GeomVertexFormat.getV3n3(), Geom.UHStatic)
        vdata.setNumRows(vertices.shape[0])

        vertex = GeomVertexWriter(vdata, "vertex")
        normal = GeomVertexWriter(vdata, "normal")

        normals = np.copy(vertices)

        for row in vertices:
            vertex.addData3(row[0], row[1], row[2])

        prim = GeomTriangles(Geom.UHStatic)
        for row in triangles:
            prim.addVertices(row[2], row[1], row[0])
            prim.closePrimitive()

        normals /= np.linalg.norm(normals, axis=1)[:, np.newaxis]
        for row in normals:
            normal.addData3(row[0], row[1], row[2])

        geom = Geom(vdata)
        geom.addPrimitive(prim)

        node = GeomNode("gnode")
        node.addGeom(geom)

        nodePath = self.render.attachNewNode(node)

        cube = self.loader.loadModel("assets/cube.glb")
        cube.reparentTo(self.render)


app = App()
app.run()
