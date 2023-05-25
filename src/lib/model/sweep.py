from lib.model.ray import Ray
import numpy as np


class Sweep:
    @classmethod
    def fromLevel2Data(cls, elevation, level2Sweep):
        rays = []

        for ray in level2Sweep:
            rays.append(Ray.fromLevel2Data(ray))

        rays = sorted(rays, key=lambda ray: ray.azimuth)

        return cls(elevation, rays)

    def __init__(self, elevation, rays):
        self.elevation = elevation
        self.rays = rays

    def foreach(self, f):
        for ray in self.rays:
            ray.foreach(self.elevation, f)

    def reflectivityMatrix(self):
        rays = np.stack(tuple(ray.reflectivity for ray in self.rays))

        # TODO this is a bit of a hack to make all of the sweeps have the same
        # number of rays. This should be cleaned up later
        if len(rays) > 500:
            return rays
        return np.repeat(rays, repeats=2, axis=0)
