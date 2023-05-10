from panda3d.core import GeomVertexData
from panda3d.core import GeomVertexFormat
from panda3d.core import GeomVertexWriter
from panda3d.core import GeomTriangles
from panda3d.core import GeomNode
from panda3d.core import Geom

import numpy as np


# This variation of generating triangles from geometry will not re-use any vertices.
# All of the normals will be calculated from the face of the triangles, so the edges
# will appear "sharp" and each face will be flat.
def trianglesToGeometry(vertices, triangles):
    vdata = GeomVertexData("name", GeomVertexFormat.getV3n3(), Geom.UHStatic)
    vdata.setNumRows(triangles.shape[0] * 3)

    vertex = GeomVertexWriter(vdata, "vertex")
    normal = GeomVertexWriter(vdata, "normal")
    primitives = GeomTriangles(Geom.UHStatic)

    i = 0
    for row in triangles:
        vec1 = vertices[row[1]] - vertices[row[0]]
        vec2 = vertices[row[2]] - vertices[row[0]]

        norm = np.cross(vec1, vec2)
        length = np.linalg.norm(norm)

        # Ignore faces that have zero area.
        # We can't calculate normals for them and they won't render.
        if length == 0:
            continue

        norm /= length

        vertex.addData3(vertices[row[0]][0], vertices[row[0]][1], vertices[row[0]][2])
        vertex.addData3(vertices[row[1]][0], vertices[row[1]][1], vertices[row[1]][2])
        vertex.addData3(vertices[row[2]][0], vertices[row[2]][1], vertices[row[2]][2])

        normal.addData3(norm[0], norm[1], norm[2])
        normal.addData3(norm[0], norm[1], norm[2])
        normal.addData3(norm[0], norm[1], norm[2])

        primitives.addVertices(i, i + 1, i + 2)
        primitives.closePrimitive()

        i += 3

    geom = Geom(vdata)
    geom.addPrimitive(primitives)

    node = GeomNode("gnode")
    node.addGeom(geom)

    return node
