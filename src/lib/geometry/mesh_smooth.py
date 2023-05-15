import numpy as np


# Removes duplicate vertices and triangles from the provided list.
# This is necessary for generating smooth geometry because the vertices
# need to be shared in order for smooth normals to be generated.
def deduplicate(vertices, triangles):
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

    return unique_vertices, unique_triangles


# This algorithm takes unoriented vertices and a list of triangles, and generates
# oriented vertices (position + normal) and updated triangles.
# For smooth shaded geometry, this means we calculate the normal for each triangle and
# add it to the normal of each vertex of the triangle, proportional to the angle at that vertex.
def orientVertices(vertices, triangles):
    vertices, triangles = deduplicate(vertices, triangles)
    normals = calcNormals(vertices, triangles)

    vertexData = np.empty((len(vertices), 6), dtype=np.float32)
    vertexData[:, :3] = vertices
    vertexData[:, 3:] = normals

    return vertexData, triangles.astype(dtype=np.uint16)


def normalize(A):
    length = np.linalg.norm(A, axis=1)
    mask = length > 0
    A[mask] /= length[mask][:, np.newaxis]
    return A


def calcNormals(vertices, triangles):
    # Vectors between all the vertices of each triangle
    vec1 = normalize(vertices[triangles[:, 1]] - vertices[triangles[:, 0]])
    vec2 = normalize(vertices[triangles[:, 2]] - vertices[triangles[:, 0]])
    vec3 = normalize(vertices[triangles[:, 2]] - vertices[triangles[:, 1]])

    # Calculate the normal for each triangle
    norm = normalize(np.cross(vec1, vec2))

    # Calculate the angles at each vertex for each triangle
    # np.einsum("ij, ij->i", vec1, vec2) calculates the dot products
    # for the corresponding vectors in each list
    a1 = np.arccos(np.einsum("ij, ij->i", vec1, vec2))[:, np.newaxis]
    a2 = np.arccos(np.einsum("ij, ij->i", vec3, -vec1))[:, np.newaxis]
    a3 = np.arccos(np.einsum("ij, ij->i", -vec2, -vec3))[:, np.newaxis]

    # Add all of the normals together at each vertex
    normals = np.zeros(vertices.shape)
    np.add.at(normals, triangles[:, 0], norm * a1)
    np.add.at(normals, triangles[:, 1], norm * a2)
    np.add.at(normals, triangles[:, 2], norm * a3)

    return normalize(normals)
