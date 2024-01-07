import math

import numpy as np
import numpy.typing as npt

from lib.model.record import Record
from lib.model.scan_data import ScanData
from lib.model.sweep_meta import SweepMeta


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

        # reflectivity scale: -20 to 80
        # velocity scale: -100 to 100
        self.reflectivityBytes = self.processData(reflectivity, -20, 80)
        self.velocityBytes = self.processData(velocity, -100, 100)

        sweepMetas = []
        for i, elevation in enumerate(elevations):
            sweepMetas.append(
                SweepMeta(
                    math.radians(elevation),
                    0,
                    math.pi / 360,
                    720,
                    ranges[0],
                    0.25,
                    reflectivity.shape[2],
                    i * reflectivity.shape[2] * 720,
                )
            )

        self.reflectivityScan = ScanData(sweepMetas, self.reflectivityBytes)
        self.velocityScan = ScanData(sweepMetas, self.velocityBytes)

    def processData(
        self,
        data: npt.NDArray[np.float32],
        scaleMin: float,
        scaleMax: float,
    ) -> bytes:
        data = data - scaleMin
        data = data / (scaleMax - scaleMin)
        data = np.clip(data, 0, 1)

        # Turn any nan into -1
        data = np.nan_to_num(data, nan=-1)

        # Get the bytes
        return data.flatten().tobytes()
