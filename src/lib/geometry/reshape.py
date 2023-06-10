import numpy as np
import numpy.typing as npt

from lib.model.scan import Scan


def reshape(vertices: npt.NDArray[np.float32], scan: Scan) -> npt.NDArray[np.float32]:
    elevation = interpolate(vertices[:, 0], np.deg2rad(scan.elevations))
    azimuth = interpolate(vertices[:, 1], np.deg2rad(scan.azimuths))
    rng = interpolate(vertices[:, 2], scan.ranges)

    sinEl = np.sin(elevation)
    cosEl = np.cos(elevation)

    sinAz = np.sin(azimuth)
    cosAz = np.cos(azimuth)

    x = rng * cosEl * sinAz
    y = rng * cosEl * cosAz
    z = rng * sinEl

    vertices[:, 0] = x
    vertices[:, 1] = y
    vertices[:, 2] = z

    return vertices


def interpolate(
    fractionalIndices: npt.NDArray[np.float32], valuemap: npt.NDArray[np.float32]
) -> npt.NDArray[np.float32]:
    floor = np.floor(fractionalIndices).astype(dtype=np.int32)
    diff = fractionalIndices - floor

    floorVal: npt.NDArray[np.float32] = valuemap[floor]
    ceilVal: npt.NDArray[np.float32] = valuemap[floor + (diff > 0)]

    return floorVal + (diff * (ceilVal - floorVal))
