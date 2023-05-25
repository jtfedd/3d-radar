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
