from src.model.serializable import Serializable
from src.util.object_equals import ObjectEquals
from src.model.ray import Ray
import struct

class Sweep(Serializable, ObjectEquals):
    @staticmethod
    def byteFormat():
        return '<i'
    
    def byteSize(self):
        size = struct.calcsize(self.byteFormat())
        for ray in self.rays:
            size += ray.byteSize()
        return size
    
    def writeBytes(self, buffer, offset):
        pointer = offset
        struct.pack_into(
            self.byteFormat(),
            buffer,
            pointer,
            len(self.rays),
        )
        pointer += struct.calcsize(self.byteFormat())

        for ray in self.rays:
            pointer = ray.writeBytes(buffer, pointer)
        
        return pointer
    
    @classmethod
    def fromSerial(cls, buffer, offset):
        pointer = offset
        numRays = struct.unpack_from(cls.byteFormat(), buffer, pointer)[0]
        pointer += struct.calcsize(cls.byteFormat())

        rays = []
        for _ in range(numRays):
            ray, pointer = Ray.fromSerial(buffer, pointer)
            rays.append(ray)

        obj = cls(rays)
        return obj, offset + obj.byteSize()

    @classmethod
    def fromLevel2Data(cls, level2Sweep):
        rays = []

        for ray in level2Sweep:
            rays.append(Ray.fromLevel2Data(ray))

        return cls(rays)

    def __init__(self, rays):
        self.rays = rays

    def foreach(self, f):
        for ray in self.rays:
            ray.foreach(f)
        