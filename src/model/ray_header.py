from src.model.serializable import Serializable
from src.util.object_equals import ObjectEquals
import struct

class RayHeader(Serializable, ObjectEquals):
    @staticmethod
    def byteFormat():
        return '<2d'
    
    def writeBytes(self, buffer, offset):
        struct.pack_into(self.byteFormat(), buffer, offset, self.azimuth, self.elevation)
        return offset + self.byteSize()
    
    @classmethod
    def fromSerial(cls, buffer, offset):
        azimuth, elevation = struct.unpack_from(cls.byteFormat(), buffer, offset)
        return cls(azimuth, elevation), offset + cls.byteSize()

    @classmethod
    def fromLevel2Data(cls, level2Ray):
        header = level2Ray[0]
        return cls(header.az_angle, header.el_angle)

    def __init__(self, azimuth, elevation):
        self.azimuth = azimuth
        self.elevation = elevation