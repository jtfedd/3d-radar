from src.model.ray_header import RayHeader
from src.model.reflectivity_header import ReflectivityHeader
from src.model.data_point import DataPoint
import numpy as np
import math

class Ray:
    def __init__(self, level2Ray):
        self.dataPoints = []

        self.header = RayHeader(level2Ray)
        self.reflectivityHeader = ReflectivityHeader(level2Ray)

        cos_el = math.cos(math.radians(self.header.elevation))
        sin_el = math.sin(math.radians(self.header.elevation))

        cos_az = math.cos(math.radians(self.header.azimuth))
        sin_az = math.sin(math.radians(self.header.azimuth))

        reflectivityData = level2Ray[4][b'REF'][1]
        for i, reflectivity in enumerate(reflectivityData):
            if np.isnan(reflectivity):
                continue

            rng = self.reflectivityHeader.range(i)

            x = rng*cos_el*sin_az
            y = rng*cos_el*cos_az
            z = rng*sin_el

            self.dataPoints.append(DataPoint(x, y, z, reflectivity))

    def foreach(self, f):
        for point in self.dataPoints:
            f(point)
