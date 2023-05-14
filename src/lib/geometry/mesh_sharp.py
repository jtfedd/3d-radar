from panda3d.core import GeomVertexData
from panda3d.core import GeomVertexFormat
from panda3d.core import GeomTriangles
from panda3d.core import GeomNode
from panda3d.core import GeomEnums
from panda3d.core import Geom

import numpy as np


# This algorithm takes unoriented vertices and a list of triangles, and generates
# oriented vertices (postition + normal) and updated triangles.
# For flat shaded geometry, this means we calculate the normal for each face and
# generate a new set of vertices for each triangle which has that normal.
# Then we generate a new set of triangles to point to the new vertices.
def orientVertices(vertices, triangles):
    # Calculate two vectors for each face
    vec1 = vertices[triangles[:, 1]] - vertices[triangles[:, 0]]
    vec2 = vertices[triangles[:, 2]] - vertices[triangles[:, 0]]

    # Calculate the cross product for each face
    norm = np.cross(vec1, vec2)
    length = np.linalg.norm(norm, axis=1)

    # Generate a mask for faces which are actually visible
    # If the normal vector has a length of zero, it means the face
    # has zero area, which means it is invisible.
    mask = length > 0

    # Normalize the normal vectors, using the mask to only affect normals
    # that are not zero-length
    norm[mask] /= length[mask].reshape(-1, 1)

    # Generate an array to hold the vertex position and normal data
    vertexData = np.empty((len(triangles) * 3, 6), dtype=np.float32)

    # Fill the vertex position data
    vertexData[:, :3] = vertices[triangles].reshape(-1, 3)

    # Fill the normal data by repeating each normal 3 times, one for each vertex
    vertexData[:, 3:] = np.repeat(norm, 3, axis=0)

    # All of the vertices are just sequential now, so generate a list of triangles
    # that references the vertices in sequential order
    triangleData = np.arange(len(triangles) * 3).reshape(-1, 3).astype(np.uint16)

    # Only return the triangles and corresponding vertices that are visible
    return vertexData[np.repeat(mask, 3)], triangleData[mask]


# This algorithm will generate vertices with normals that are specific per face.
# The vertices for each face will have the normal of the face.
# This results in a mesh that looks "sharp" and each face is flat.
def trianglesToGeometry(vertices, triangles):
    vertices, triangles = orientVertices(vertices, triangles)

    vdata = GeomVertexData("vdata", GeomVertexFormat.getV3n3(), Geom.UHStatic)
    vdata.uncleanSetNumRows(len(vertices))
    vArray = vdata.modifyArray(0)
    vView = memoryview(vArray).cast("B").cast("f")
    vView[:] = vertices.flatten()

    trisData = GeomTriangles(Geom.UHStatic)
    trisData.setIndexType(GeomEnums.NT_uint16)
    trisArray = trisData.modifyVertices()
    trisArray.uncleanSetNumRows(len(triangles) * 3)
    tView = memoryview(trisArray).cast("B").cast("H")
    tView[:] = triangles.flatten()

    geom = Geom(vdata)
    geom.addPrimitive(trisData)

    node = GeomNode("gnode")
    node.addGeom(geom)

    return node
