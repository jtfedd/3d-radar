from panda3d.core import GeomVertexData
from panda3d.core import GeomVertexFormat
from panda3d.core import GeomVertexWriter
from panda3d.core import GeomTriangles
from panda3d.core import GeomNode
from panda3d.core import Geom

import numpy as np


# WIP generates smooth geometry
def trianglesToGeometry(vertices, triangles):
    # Not all of the vertices are unique. This means there are sometimes
    # multiple vertices at the same location, but they will not share normals.
    # Remove duplicate vertices before continuing.
    unique_vertices, vertex_mapping = np.unique(vertices, axis=0, return_inverse=True)

    # Now we need to map the triangles to refer to the correct vertex in the
    # unique vertex list.
    mapped_triangles = np.vectorize(lambda x: vertex_mapping[x])(triangles)

    # After mapping the triangles it's possible that some of them are now identical.
    # Remove triangles that are the same.
    unique_triangles = np.unique(mapped_triangles, axis=0)

    # Replace our input with the refined output
    vertices = unique_vertices
    triangles = unique_triangles

    # Generate the geometry
    vdata = GeomVertexData("name", GeomVertexFormat.getV3n3(), Geom.UHStatic)
    vdata.setNumRows(vertices.shape[0])

    vertexWriter = GeomVertexWriter(vdata, "vertex")
    normalWriter = GeomVertexWriter(vdata, "normal")

    normals = np.zeros(vertices.shape)

    for row in vertices:
        vertexWriter.addData3(row[0], row[1], row[2])

    prim = GeomTriangles(Geom.UHStatic)
    for row in triangles:
        vec1 = vertices[row[1]] - vertices[row[0]]
        vec2 = vertices[row[2]] - vertices[row[0]]

        norm = np.cross(vec1, vec2)
        length = np.linalg.norm(norm)

        # We can ignore faces that have zero area
        if length == 0:
            continue

        norm /= length
        normals[row[0]] += norm
        normals[row[1]] += norm
        normals[row[2]] += norm

        prim.addVertices(row[0], row[1], row[2])
        prim.closePrimitive()

    normals /= np.linalg.norm(normals, axis=1)[:, np.newaxis]
    for row in normals:
        normalWriter.addData3(row[0], row[1], row[2])

    geom = Geom(vdata)
    geom.addPrimitive(prim)

    node = GeomNode("gnode")
    node.addGeom(geom)

    return node
