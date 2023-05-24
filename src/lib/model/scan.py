from lib.model.sweep import Sweep
from lib.model.ray import Ray
import numpy as np


class Scan:
    @classmethod
    def fromLevel2Data(cls, level2File, station, date, time):
        sweeps = []

        elevations = []
        for elevationHeader, sweep in zip(level2File.vcp_info.els, level2File.sweeps):
            # Skip any elevations for which we have already accepted a sweep
            if np.any(np.isclose(elevationHeader.el_angle, elevations)):
                continue

            # Some elevations have a batch config, where reflectivity and velocity are recorded together.
            # Others have a split config, where reflectivity and velocity are recorded on separate passes.
            # We will take the sweeps with batch config and the reflectivity pass from the split cuts.
            isReflectivitySweep = (
                elevationHeader.channel_config == "Constant Phase"
                or (
                    elevationHeader.channel_config == "SZ2 Phase"
                    and elevationHeader.waveform == "Contiguous Surveillance"
                )
            )

            if not isReflectivitySweep:
                continue

            elevations.append(elevationHeader.el_angle)
            sweeps.append(Sweep.fromLevel2Data(elevationHeader.el_angle, sweep))

        # TODO this is a bit of a hack to get an empty sweep on the top and bottom.
        # This is necessary to generate closed geometry on the top and bottom.
        bottomRays = []
        topRays = []

        for ray in sweeps[0].rays:
            emptyRef = np.empty(sweeps[0].rays[0].reflectivity.shape)
            emptyRef[:] = np.nan
            bottomRays.append(Ray(ray.azimuth, ray.first, ray.spacing, emptyRef))
        for ray in sweeps[0].rays:
            emptyRef = np.empty(sweeps[0].rays[0].reflectivity.shape)
            emptyRef[:] = np.nan
            topRays.append(Ray(ray.azimuth, ray.first, ray.spacing, emptyRef))

        sweeps.insert(0, Sweep(0, bottomRays))
        sweeps.append(Sweep(elevations[-1] + elevations[-1] - elevations[-2], topRays))

        return cls(sweeps, station, date, time)

    def __init__(self, sweeps, station, date, time):
        self.sweeps = sweeps
        self.station = station
        self.date = date
        self.time = time

        self.sweeps = sorted(self.sweeps, key=lambda sweep: sweep.elevation)

    def foreach(self, f):
        for sweep in self.sweeps:
            sweep.foreach(f)

    def points(self):
        points = []
        self.foreach(lambda p: points.append(p))
        return points

    def reflectivityMatrix(self):
        sweeps = [sweep.reflectivityMatrix() for sweep in self.sweeps]
        return np.stack(sweeps)
