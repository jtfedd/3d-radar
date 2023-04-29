from src.model.serializable import Serializable
from src.util.object_equals import ObjectEquals
from src.model.ray_header import RayHeader
from src.model.reflectivity_header import ReflectivityHeader
from src.model.data_point import DataPoint
import numpy as np
import struct
import math

class Ray(Serializable, ObjectEquals):
    @staticmethod
    def byteFormat():
        return '<i'
    
    def byteSize(self):
        size = struct.calcsize(self.byteFormat())
        size +=  self.header.byteSize() 
        size += self.reflectivityHeader.byteSize()
        for point in self.dataPoints:
            size += point.byteSize()
        return size
    
    def writeBytes(self, buffer, offset):
        pointer = offset
        struct.pack_into(self.byteFormat(), buffer, pointer, len(self.dataPoints))
        pointer += struct.calcsize(self.byteFormat())

        pointer = self.header.writeBytes(buffer, pointer)
        pointer = self.reflectivityHeader.writeBytes(buffer, pointer)
        for dataPoint in self.dataPoints:
            pointer = dataPoint.writeBytes(buffer, pointer)

        return pointer
    
    @classmethod
    def fromSerial(cls, buffer, offset):
        pointer = offset
        numPoints = struct.unpack_from(cls.byteFormat(), buffer, pointer)[0]
        pointer += struct.calcsize(cls.byteFormat())

        header, pointer = RayHeader.fromSerial(buffer, pointer)
        reflectivityHeader, pointer = ReflectivityHeader.fromSerial(buffer, pointer)
        dataPoints = []
        for _ in range(numPoints):
            dataPoint, pointer = DataPoint.fromSerial(buffer, pointer)
            dataPoints.append(dataPoint)

        obj = cls(header, reflectivityHeader, dataPoints)
        return obj, offset + obj.byteSize()

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
