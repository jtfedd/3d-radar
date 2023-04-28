from src.model.serializable import Serializable
from src.util.object_equals import ObjectEquals
import struct

class DataPoint(Serializable, ObjectEquals):
    @staticmethod
    def byteFormat():
        return '<4d'
    
    def writeBytes(self, buffer, offset):
        struct.pack_into(self.byteFormat(), buffer, offset, self.x, self.y, self.z, self.reflectivity)
        return offset + self.byteSize()
    
    @classmethod
    def fromSerial(cls, buffer, offset):
        x, y, z, reflectivity = struct.unpack_from(cls.byteFormat(), buffer, offset)
        return cls(x, y, z, reflectivity), offset + cls.byteSize()

    def __init__(self, x, y, z, reflectivity):
        self.x = x
        self.y = y
        self.z = z

        self.reflectivity = reflectivity
