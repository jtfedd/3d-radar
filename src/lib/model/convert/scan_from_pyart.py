from typing import Dict, List

import numpy as np
import numpy.typing as npt
import pyart

from lib.model.record import Record
from lib.model.scan import Scan


class RayData:
    def __init__(self, azimuth: float, data: npt.NDArray[np.float32]):
        self.azimuth = azimuth
        self.data = np.pad(
            data,
            (1, 1),
            mode="constant",
            constant_values=(np.nan),
        )


class SweepData:
    def __init__(self, elevation: float, data: npt.NDArray[np.float32]):
        self.elevation = elevation
        self.data = data

    def hasData(self) -> bool:
        return np.count_nonzero(~np.isnan(self.data)) == 0


def scanFromRadar(record: Record, radar: pyart.core.Radar) -> Scan:
    print(radar.nsweeps)

    elevations = radar.fixed_angle["data"]

    first = radar.range["meters_to_center_of_first_gate"] / 1000.0
    spacing = radar.range["meters_between_gates"] / 1000.0

    raysPerSweep = radar.rays_per_sweep["data"]

    refLayers: Dict[int, SweepData] = {}
    velLayers: Dict[int, SweepData] = {}

    for i in range(radar.nsweeps):
        azimuths = radar.get_azimuth(i)
        elevation = elevations[i]
        rays = raysPerSweep[i]

        refData = radar.get_field(i, "reflectivity").filled(np.nan)
        velData = radar.get_field(i, "velocity").filled(np.nan)

        refRays: List[RayData] = []
        velRays: List[RayData] = []

        for j in range(rays):
            azimuth = azimuths[j]
            refRay = refData[j]
            velRay = velData[j]

            refRays.append(RayData(azimuth, refRay))
            velRays.append(RayData(azimuth, velRay))

        refRays.sort(key=lambda r: r.azimuth)
        velRays.sort(key=lambda r: r.azimuth)

        refComposite = np.stack(tuple(ray.data for ray in refRays))
        velComposite = np.stack(tuple(ray.data for ray in velRays))

        # Hack to make all sweeps have same number of rays
        if rays < 500:
            refComposite = np.repeat(refComposite, repeats=2, axis=0)
            velComposite = np.repeat(velComposite, repeats=2, axis=0)

        if elevation in refLayers:
            if not refLayers[elevation].hasData():
                refLayers[elevation] = SweepData(elevation, refComposite)
        else:
            refLayers[elevation] = SweepData(elevation, refComposite)

        if elevation in velLayers:
            if not velLayers[elevation].hasData():
                velLayers[elevation] = SweepData(elevation, velComposite)
        else:
            velLayers[elevation] = SweepData(elevation, velComposite)

    reflectivityLayers = [
        sweep.data
        for sweep in sorted(refLayers.values(), key=lambda sweep: sweep.elevation)
    ]

    velocityLayers = [
        sweep.data
        for sweep in sorted(velLayers.values(), key=lambda sweep: sweep.elevation)
    ]

    # Add empty sweep on top and bottom
    emptyRef = np.empty((720, radar.ngates + 2), dtype=np.float32)
    emptyRef[:] = np.nan

    reflectivityLayers.insert(0, emptyRef)
    reflectivityLayers.append(emptyRef)

    velocityLayers.insert(0, emptyRef)
    velocityLayers.append(emptyRef)

    azimuths = np.linspace(0, 359.5, 720, dtype=np.float32)
    ranges = np.linspace(
        first, first + (radar.ngates + 2) * spacing, radar.ngates + 2, dtype=np.float32
    )

    els = sorted(refLayers.keys())
    els.insert(0, 0)
    els.append(els[-1] + els[-1] - els[-2])
    elevations = np.array(els, dtype=np.float32)

    reflectivity = np.stack(reflectivityLayers)
    velocity = np.stack(velocityLayers)

    return Scan(record, elevations, azimuths, ranges, reflectivity, velocity)
