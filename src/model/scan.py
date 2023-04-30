from src.model.serializable import Serializable
from src.util.object_equals import ObjectEquals
from src.model.sweep import Sweep
import struct
import datetime

class Scan(Serializable, ObjectEquals):
    @staticmethod
    def byteFormat() -> str:
        return '<7i4s'
    
    def byteSize(self):
        size = struct.calcsize(self.byteFormat())
        for sweep in self.sweeps:
            size += sweep.byteSize()
        return size
    
    def writeBytes(self, buffer, offset):
        pointer = offset
        struct.pack_into(
            self.byteFormat(),
            buffer,
            pointer,
            self.date.year,
            self.date.month,
            self.date.day,
            self.time.hour,
            self.time.minute,
            self.time.second,
            len(self.sweeps),
            bytes(self.station, 'utf-8'),
        )
        pointer += struct.calcsize(self.byteFormat())

        for sweep in self.sweeps:
            pointer = sweep.writeBytes(buffer, pointer)

        return pointer
    
    @classmethod
    def fromSerial(cls, buffer, offset):
        pointer = offset
        year, month, day, hour, minute, second, numSweeps, stationBytes = struct.unpack_from(cls.byteFormat(), buffer, pointer)
        pointer += struct.calcsize(cls.byteFormat())

        station = stationBytes.rstrip(b'\x00').decode("utf_8")
        date = datetime.date(year=year, month=month, day=day)
        time = datetime.time(hour=hour, minute=minute, second=second)

        sweeps = []
        for _ in range(numSweeps):
            sweep, pointer = Sweep.fromSerial(buffer, pointer)
            sweeps.append(sweep)

        obj = cls(sweeps, station, date, time)
        return obj, offset + obj.byteSize()

    @classmethod
    def fromLevel2Data(cls, level2File, station, date, time):
        sweeps = []

        for sweep in level2File.sweeps:
            sweeps.append(Sweep.fromLevel2Data(sweep))
        
        return cls(sweeps, station, date, time)

    def __init__(self, sweeps, station, date, time):
        self.sweeps = sweeps
        self.station = station
        self.date = date
        self.time = time
    
    def foreach(self, f):
        for sweep in self.sweeps:
            sweep.foreach(f)

    def points(self):
        points = []
        self.foreach(lambda p : points.append(p))
        return points