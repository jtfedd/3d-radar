from typing import Tuple

import numpy as np
import numpy.typing as npt


# This algorithm takes unoriented vertices and a list of triangles, and generates
# oriented vertices (postition + normal) and updated triangles.
# For flat shaded geometry, this means we calculate the normal for each triangle and
# generate a new set of vertices for each triangle which has that normal.
# Then we generate a new set of triangles to point to the new vertices.
def orientVertices(
    vertices: npt.NDArray[np.float32], triangles: npt.NDArray[np.uint32]
) -> Tuple[npt.NDArray[np.float32], npt.NDArray[np.uint32]]:
    # Calculate two vectors for each triangle
    vec1 = vertices[triangles[:, 1]] - vertices[triangles[:, 0]]
    vec2 = vertices[triangles[:, 2]] - vertices[triangles[:, 0]]

    # Calculate the cross product for each triangle
    norm = np.cross(vec1, vec2)
    length = np.linalg.norm(norm, axis=1)

    # Generate a mask for triangles which are actually visible
    # If the normal vector has a length of zero, it means the triangle
    # has zero area, which means it is invisible.
    mask = length > 0

    # Normalize the normal vectors, using the mask to only affect normals
    # that are not zero-length
    norm[mask] /= length[mask][:, np.newaxis]

    # Generate an array to hold the vertex position and normal data
    vertexData = np.empty((len(triangles) * 3, 6), dtype=np.float32)

    # Fill the vertex position data
    vertexData[:, :3] = vertices[triangles].reshape(-1, 3)

    # Fill the normal data by repeating each normal 3 times, one for each vertex
    vertexData[:, 3:] = np.repeat(norm, 3, axis=0)

    # All of the vertices are just sequential now, so generate a list of triangles
    # that references the vertices in sequential order
    triangleData = np.arange(len(triangles) * 3, dtype=np.uint32).reshape(-1, 3)

    return vertexData, triangleData
