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
        vdata.setNumRows(triangles.shape[0] * 3)

        vertex = GeomVertexWriter(vdata, "vertex")
        normal = GeomVertexWriter(vdata, "normal")

        # for row in vertices:
        #     vertex.addData3(row[0], row[1], row[2])

        prim = GeomTriangles(Geom.UHStatic)
        i = 0
        for row in triangles:
            vec1 = vertices[row[2]] - vertices[row[0]]
            vec2 = vertices[row[1]] - vertices[row[0]]

            xp = np.cross(vec1, vec2)
            length = np.linalg.norm(xp)

            if length == 0:
                continue

            norm = xp / length

            vertex.addData3(
                vertices[row[0]][0], vertices[row[0]][1], vertices[row[0]][2]
            )
            vertex.addData3(
                vertices[row[1]][0], vertices[row[1]][1], vertices[row[1]][2]
            )
            vertex.addData3(
                vertices[row[2]][0], vertices[row[2]][1], vertices[row[2]][2]
            )

            normal.addData3(norm[0], norm[1], norm[2])
            normal.addData3(norm[0], norm[1], norm[2])
            normal.addData3(norm[0], norm[1], norm[2])

            prim.addVertices(i, i + 2, i + 1)
            prim.closePrimitive()

            i += 3

        geom = Geom(vdata)
        geom.addPrimitive(prim)

        node = GeomNode("gnode")
        node.addGeom(geom)

        nodePath = self.render.attachNewNode(node)

        cube = self.loader.loadModel("assets/cube.glb")
        cube.reparentTo(self.render)


app = App()
app.run()
