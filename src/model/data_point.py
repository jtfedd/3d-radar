from src.model.serializable import Serializable
import struct

class DataPoint(Serializable):
    @staticmethod
    def byteFormat():
        return '<4d'
    
    @staticmethod
    def byteSize():
        return struct.calcsize(DataPoint.byteFormat())
    
    def writeBytes(self, buffer, offset):
        struct.pack_into(self.byteFormat(), buffer, offset, self.x, self.y, self.z, self.reflectivity)
        return offset + self.byteSize()
    
    @classmethod
    def fromSerial(cls, buffer, offset):
        x, y, z, reflectivity = struct.unpack_from(cls.byteFormat(), buffer, offset)
        return cls(x, y, z, reflectivity), offset + cls.byteSize()
    
    def __eq__(self, other):
        if not isinstance(other, DataPoint):
            return NotImplemented
        return self.x == other.x and self.y == other.y and self.z == other.z and self.reflectivity == other.reflectivity

    def __init__(self, x, y, z, reflectivity):
        self.x = x
        self.y = y
        self.z = z

        self.reflectivity = reflectivity
