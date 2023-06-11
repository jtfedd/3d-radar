import math
from enum import Enum
from typing import List

import numpy as np
import numpy.typing as npt
from metpy.io import Level2File

from lib.model.record import Record
from lib.model.scan import Scan

RAY_LENGTH = 2000


class DataType(Enum):
    REFLECTIVITY = b"REF"
    VELOCITY = b"VEL"


class RayData:
    def __init__(
        self,
        azimuth: float,
        first: float,
        spacing: float,
        data: npt.NDArray[np.float32],
    ):
        self.azimuth = azimuth

        self.spacing = spacing
        self.first = first - spacing

        self.data = np.pad(
            data,
            (1, RAY_LENGTH - data.shape[0]),
            mode="constant",
            constant_values=(np.nan),
        )


class SweepData:
    def __init__(
        self, elevation: float, config: str, waveform: str, rays: List[RayData]
    ):
        self.elevation = elevation
        self.config = config
        self.waveform = waveform
        self.rays = rays

    def isConstantPhase(self) -> bool:
        return self.config == "Constant Phase"

    def isSplitPhase(self) -> bool:
        return self.config == "SZ2 Phase"

    def isReflectivitySweep(self) -> bool:
        return self.isConstantPhase() or (
            self.isSplitPhase() and self.waveform == "Contiguous Surveillance"
        )

    def isVelocitySweep(self) -> bool:
        return self.isConstantPhase() or (
            self.isSplitPhase() and ("Doppler" in self.waveform)
        )

    def isForDataType(self, dataType: DataType) -> bool:
        match dataType:
            case DataType.REFLECTIVITY:
                return self.isReflectivitySweep()
            case DataType.VELOCITY:
                return self.isVelocitySweep()
        return False


def dataFromMetpy(level2File: Level2File, dataType: DataType) -> List[SweepData]:
    sweeps: List[SweepData] = []

    for elevationHeader, sweep in zip(level2File.vcp_info.els, level2File.sweeps):
        elevation: float = elevationHeader.el_angle

        if np.any(np.isclose(elevation, [sweep.elevation for sweep in sweeps])):
            continue

        config: str = elevationHeader.channel_config
        waveform: str = elevationHeader.waveform

        rays: List[RayData] = []

        for ray in sweep:
            if dataType not in ray[4]:
                continue

            header = ray[0]
            reflectivityHeader = ray[4][dataType][0]

            azimuth: float = math.radians(header.az_angle)
            first: float = reflectivityHeader.first_gate
            spacing: float = reflectivityHeader.gate_width
            data: npt.NDArray[np.float32] = ray[4][dataType][1].astype(np.float32)

            rays.append(RayData(azimuth, first, spacing, data))

        rays = sorted(rays, key=lambda ray: ray.azimuth)
        sweep = SweepData(elevation, config, waveform, rays)

        if not sweep.isForDataType(dataType):
            continue

        sweeps.append(sweep)

    return sorted(sweeps, key=lambda sweep: sweep.elevation)


def scanFromLevel2Data(record: Record, data: Level2File) -> Scan:
    reflectivitySweeps = dataFromMetpy(data, DataType.REFLECTIVITY)
    velocitySweeps = dataFromMetpy(data, DataType.VELOCITY)

    reflectivityElevations = [sweep.elevation for sweep in reflectivitySweeps]
    velocityElevations = [sweep.elevation for sweep in velocitySweeps]

    if not np.allclose(reflectivityElevations, velocityElevations):
        raise Exception("Reflectivity and velocity data do not match")

    reflectivityLayers = []
    velocityLayers = []

    first: float = 0
    spacing: float = 0

    for sweep in reflectivitySweeps:
        first = sweep.rays[0].first
        spacing = sweep.rays[0].spacing
        sweepReflectivity = np.stack(tuple(ray.data for ray in sweep.rays))

        # TODO this is a bit of a hack to make all of the sweeps have the same
        # number of rays. This should be cleaned up later
        if len(sweep.rays) < 500:
            sweepReflectivity = np.repeat(sweepReflectivity, repeats=2, axis=0)

        reflectivityLayers.append(sweepReflectivity)

    for sweep in velocitySweeps:
        first = sweep.rays[0].first
        spacing = sweep.rays[0].spacing
        sweepVelocity = np.stack(tuple(ray.data for ray in sweep.rays))

        if len(sweep.rays) < 500:
            sweepVelocity = np.repeat(sweepVelocity, repeats=2, axis=0)

        velocityLayers.append(sweepVelocity)

    # TODO this is a bit of a hack to get an empty sweep on the top and bottom.
    # This is necessary to generate closed geometry on the top and bottom.
    emptyRef = np.empty(reflectivityLayers[0].shape, dtype=np.float32)
    emptyRef[:] = np.nan

    reflectivityLayers.insert(0, emptyRef)
    reflectivityLayers.append(emptyRef)

    velocityLayers.insert(0, emptyRef)
    velocityLayers.append(emptyRef)

    reflectivityElevations.insert(0, 0)
    reflectivityElevations.append(
        reflectivityElevations[-1]
        + reflectivityElevations[-1]
        - reflectivityElevations[-2]
    )
    elevations = np.array(reflectivityElevations, dtype=np.float32)

    azimuths = np.linspace(0, 359.5, 720, dtype=np.float32)
    ranges = np.linspace(
        first, first + RAY_LENGTH * spacing, RAY_LENGTH + 1, dtype=np.float32
    )

    reflectivity = np.stack(reflectivityLayers)
    velocity = np.stack(velocityLayers)

    return Scan(record, elevations, azimuths, ranges, reflectivity, velocity)
