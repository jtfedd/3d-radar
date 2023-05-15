from lib.geometry import normals_sharp
from lib.geometry import normals_smooth
from lib.geometry import triangles_to_geometry


import mcubes


def getIsosurface(data, value):
    vertices, triangles = mcubes.marching_cubes(data, value)

    # The vertices that come from marching cubes are "wound" the wrong way, causing
    # the triangles to all be facing inward instead of outward.
    # If we swap columns 1 and 2, leaving column 0 in place, this reverses the order
    # and causes the triangles to be "wound" the correct way. This makes the rest of
    # the code a little less confusing.
    triangles[:, [1, 2]] = triangles[:, [2, 1]]

    return vertices, triangles


def getGeometry(data, value, smooth=False):
    vertices, triangles = getIsosurface(data, value)

    if smooth:
        vertices, triangles = normals_smooth.orientVertices(vertices, triangles)
    else:
        vertices, triangles = normals_sharp.orientVertices(vertices, triangles)

    return triangles_to_geometry.trianglesToGeometry(vertices, triangles)
