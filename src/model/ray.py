from src.model.ray_header import RayHeader
from src.model.reflectivity_header import ReflectivityHeader
from src.model.data_point import DataPoint
import numpy as np
import math

class Ray:
    @classmethod
    def fromLevel2Data(cls, level2Ray):
        dataPoints = []

        header = RayHeader.fromLevel2Data(level2Ray)
        reflectivityHeader = ReflectivityHeader.fromLevel2Data(level2Ray)

        cos_el = math.cos(math.radians(header.elevation))
        sin_el = math.sin(math.radians(header.elevation))

        cos_az = math.cos(math.radians(header.azimuth))
        sin_az = math.sin(math.radians(header.azimuth))

        reflectivityData = level2Ray[4][b'REF'][1]
        for i, reflectivity in enumerate(reflectivityData):
            if np.isnan(reflectivity):
                continue

            rng = reflectivityHeader.range(i)

            x = rng*cos_el*sin_az
            y = rng*cos_el*cos_az
            z = rng*sin_el

            dataPoints.append(DataPoint(x, y, z, reflectivity))

        return cls(header, reflectivityHeader, dataPoints)

    def __init__(self, header, reflectivityHeader, dataPoints):
        self.header = header
        self.reflectivityHeader = reflectivityHeader
        self.dataPoints = dataPoints

    def foreach(self, f):
        for point in self.dataPoints:
            f(point)
