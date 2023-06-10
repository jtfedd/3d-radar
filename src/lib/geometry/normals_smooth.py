from typing import Tuple

import numpy as np
import numpy.typing as npt


# Removes duplicate vertices and triangles from the provided list.
# This is necessary for generating smooth geometry because the vertices
# need to be shared in order for smooth normals to be generated.
def deduplicate(
    vertices: npt.NDArray[np.float32], triangles: npt.NDArray[np.uint32]
) -> Tuple[npt.NDArray[np.float32], npt.NDArray[np.uint32]]:
    # Not all of the vertices are unique. This means there are sometimes
    # multiple vertices at the same location, but they will not share normals.
    # Remove duplicate vertices before continuing.
    uniqueVertices, vertexMapping = np.unique(vertices, axis=0, return_inverse=True)

    # Now we need to map the triangles to refer to the correct vertex in the
    # unique vertex list.
    mappedTriangles = np.vectorize(lambda x: vertexMapping[x])(triangles)

    # After mapping the triangles it's possible that some of them are now identical.
    # Remove triangles that are the same.
    uniqueTriangles = np.unique(mappedTriangles, axis=0)

    return uniqueVertices, uniqueTriangles


# This algorithm takes unoriented vertices and a list of triangles, and generates
# oriented vertices (position + normal) and updated triangles.
# For smooth shaded geometry, this means we calculate the normal for each triangle as
# the sum of the weighted normals of the triangles around the vertex, where the weights
# are calculated as the angles of the triangle at the vertex
def orientVertices(
    vertices: npt.NDArray[np.float32], triangles: npt.NDArray[np.uint32]
) -> Tuple[npt.NDArray[np.float32], npt.NDArray[np.uint32]]:
    vertices, triangles = deduplicate(vertices, triangles)
    normals = calcNormals(vertices, triangles)

    vertexData = np.empty((len(vertices), 6), dtype=np.float32)
    vertexData[:, :3] = vertices
    vertexData[:, 3:] = normals

    return vertexData, triangles


def normalize(vectors: npt.NDArray[np.float32]) -> npt.NDArray[np.float32]:
    length = np.linalg.norm(vectors, axis=1)
    mask = length > 0
    vectors[mask] /= length[mask][:, np.newaxis]
    return vectors


def calcNormals(
    vertices: npt.NDArray[np.float32], triangles: npt.NDArray[np.uint32]
) -> npt.NDArray[np.float32]:
    # Vectors between all the vertices of each triangle
    vec1 = normalize(vertices[triangles[:, 1]] - vertices[triangles[:, 0]])
    vec2 = normalize(vertices[triangles[:, 2]] - vertices[triangles[:, 0]])
    vec3 = normalize(vertices[triangles[:, 2]] - vertices[triangles[:, 1]])

    # Calculate the normal for each triangle
    norm = normalize(np.cross(vec1, vec2))

    # Calculate the angles at each vertex for each triangle
    # np.einsum("ij, ij->i", vec1, vec2) calculates the dot products
    # for the corresponding vectors in each list
    angle1 = np.arccos(np.einsum("ij, ij->i", vec1, vec2))[:, np.newaxis]
    angle2 = np.arccos(np.einsum("ij, ij->i", vec3, -vec1))[:, np.newaxis]
    angle3 = np.arccos(np.einsum("ij, ij->i", -vec2, -vec3))[:, np.newaxis]

    # Add all of the normals together at each vertex
    normals = np.zeros(vertices.shape, dtype=np.float32)
    np.add.at(normals, triangles[:, 0], norm * angle1)
    np.add.at(normals, triangles[:, 1], norm * angle2)
    np.add.at(normals, triangles[:, 2], norm * angle3)

    return normalize(normals)
