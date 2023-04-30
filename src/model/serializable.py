from abc import ABC, abstractmethod

import struct


class Serializable(ABC):
    @staticmethod
    @abstractmethod
    def byteFormat() -> str:
        pass

    def byteSize(self):
        return struct.calcsize(self.byteFormat())

    @abstractmethod
    def writeBytes(self, buffer, offset) -> int:
        pass

    @classmethod
    @abstractmethod
    def fromSerial(cls, buffer, offset):
        pass

    @classmethod
    def deserialize(cls, buffer):
        obj, _ = cls.fromSerial(buffer, 0)
        return obj

    def serialize(self):
        buffer = bytearray(self.byteSize())
        self.writeBytes(buffer, 0)
        return buffer
