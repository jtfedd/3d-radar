from panda3d.core import GeomVertexData
from panda3d.core import GeomVertexFormat
from panda3d.core import GeomVertexWriter
from panda3d.core import GeomTriangles
from panda3d.core import GeomNode
from panda3d.core import Geom

import numpy as np


# WIP generates smooth geometry
def trianglesToGeometry(vertices, triangles):
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

    return node
