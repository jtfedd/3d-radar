import numpy as np
import numpy.typing as npt

from lib.model.record import Record


class Scan:
    def __init__(
        self,
        record: Record,
        elevations: npt.NDArray[np.float32],
        azimuths: npt.NDArray[np.float32],
        ranges: npt.NDArray[np.float32],
        reflectivity: npt.NDArray[np.float32],
        velocity: npt.NDArray[np.float32],
    ):
        self.record = record
        self.elevations = elevations
        self.azimuths = azimuths
        self.ranges = ranges

        self.reflectivity = reflectivity
        self.velocity = velocity
