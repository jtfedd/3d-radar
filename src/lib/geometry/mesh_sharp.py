from panda3d.core import GeomVertexData
from panda3d.core import GeomVertexFormat
from panda3d.core import GeomTriangles
from panda3d.core import GeomNode
from panda3d.core import GeomEnums
from panda3d.core import Geom

import numpy as np


# This algorithm will generate vertices with normals that are specific per face.
# The vertices for each face will have the normal of the face.
# This results in a mesh that looks "sharp" and each face is flat.
def trianglesToGeometry(vertices, triangles):
    numVertices = triangles.shape[0] * 3
    numFaces = triangles.shape[0]

    vertexData = np.empty((numVertices, 6), dtype=np.float32)
    facesData = np.empty((numFaces, 3), dtype=np.uint16)

    vertexIndex = 0
    faceIndex = 0
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

        vertexData[vertexIndex] = [
            vertices[row[0]][0],
            vertices[row[0]][1],
            vertices[row[0]][2],
            norm[0],
            norm[1],
            norm[2],
        ]
        vertexData[vertexIndex + 1] = [
            vertices[row[1]][0],
            vertices[row[1]][1],
            vertices[row[1]][2],
            norm[0],
            norm[1],
            norm[2],
        ]
        vertexData[vertexIndex + 2] = [
            vertices[row[2]][0],
            vertices[row[2]][1],
            vertices[row[2]][2],
            norm[0],
            norm[1],
            norm[2],
        ]

        facesData[faceIndex] = [vertexIndex, vertexIndex + 1, vertexIndex + 2]

        vertexIndex += 3
        faceIndex += 1

    vdata = GeomVertexData("vdata", GeomVertexFormat.getV3n3(), Geom.UHStatic)
    vdata.uncleanSetNumRows(numVertices)
    vArray = vdata.modifyArray(0)
    vView = memoryview(vArray).cast("B").cast("f")
    vView[:] = vertexData.flatten()

    trisData = GeomTriangles(Geom.UHStatic)
    trisData.setIndexType(GeomEnums.NT_uint16)
    trisArray = trisData.modifyVertices()
    trisArray.uncleanSetNumRows(numFaces * 3)
    tView = memoryview(trisArray).cast("B").cast("H")
    tView[:] = facesData.flatten()

    geom = Geom(vdata)
    geom.addPrimitive(trisData)

    node = GeomNode("gnode")
    node.addGeom(geom)

    return node
