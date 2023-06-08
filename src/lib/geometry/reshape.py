import numpy as np

from lib.model.scan import Scan


def reshape(vertices, scan: Scan):
    elevation = interpolate(vertices[:, 0], np.deg2rad(scan.elevations))
    azimuth = interpolate(vertices[:, 1], np.deg2rad(scan.azimuths))
    rng = interpolate(vertices[:, 2], scan.ranges)

    sin_el = np.sin(elevation)
    cos_el = np.cos(elevation)

    sin_az = np.sin(azimuth)
    cos_az = np.cos(azimuth)

    x = rng * cos_el * sin_az
    y = rng * cos_el * cos_az
    z = rng * sin_el

    vertices[:, 0] = x
    vertices[:, 1] = y
    vertices[:, 2] = z

    return vertices


def interpolate(fractionalIndices, valuemap):
    floor = np.floor(fractionalIndices).astype(dtype=np.int32)
    diff = fractionalIndices - floor

    floorVal = valuemap[floor]
    ceilVal = valuemap[floor + (diff > 0)]

    return floorVal + (diff * (ceilVal - floorVal))
