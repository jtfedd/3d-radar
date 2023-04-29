from src.model.serializable import Serializable
from src.util.object_equals import ObjectEquals
import struct

class ReflectivityHeader(Serializable, ObjectEquals):
    @staticmethod
    def byteFormat():
        return '<i2d'
    
    def writeBytes(self, buffer, offset):
        struct.pack_into(self.byteFormat(), buffer, offset, self.numGates, self.gateWidth, self.firstGate)
        return offset + self.byteSize()
    
    @classmethod
    def fromSerial(cls, buffer, offset):
        numGates, gateWidth, firstGate = struct.unpack_from(cls.byteFormat(), buffer, offset)
        return cls(numGates, gateWidth, firstGate), offset + cls.byteSize()

    @classmethod
    def fromLevel2Data(cls, level2Ray):
        header = level2Ray[4][b'REF'][0]
        return cls(header.num_gates, header.gate_width, header.first_gate)

    def __init__(self, numGates, gateWidth, firstGate):
        self.numGates = numGates
        self.gateWidth = gateWidth
        self.firstGate = firstGate

    def range(self, i):
        return self.firstGate + (self.gateWidth * i)