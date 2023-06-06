from lib.model.scan import Scan
from lib.model.record import Record
import struct
import datetime
import numpy as np

recordFormat = "<d4s"
scanFormat = "<5I"
recordFormatSize = struct.calcsize(recordFormat)
scanFormatSize = struct.calcsize(scanFormat)


def serializeScan(scan: Scan):
    buffer = serializeRecord(scan.record)

    elevationBytes = scan.elevations.tobytes()
    azimuthBytes = scan.azimuths.tobytes()
    rangesBytes = scan.ranges.tobytes()
    reflectivityBytes = scan.reflectivity.tobytes()
    velocityBytes = scan.velocity.tobytes()

    buffer += struct.pack(
        scanFormat,
        len(elevationBytes),
        len(azimuthBytes),
        len(rangesBytes),
        len(reflectivityBytes),
        len(velocityBytes),
    )

    buffer += elevationBytes
    buffer += azimuthBytes
    buffer += rangesBytes
    buffer += reflectivityBytes
    buffer += velocityBytes

    return buffer


def serializeRecord(record: Record):
    return struct.pack(
        recordFormat,
        int(record.time.timestamp()),
        bytes(record.station, "utf-8"),
    )


def deserializeRecord(buffer, offset=0):
    unixTime, stationBytes = struct.unpack_from(recordFormat, buffer, offset=offset)
    station = stationBytes.rstrip(b"\x00").decode("utf-8")
    time = datetime.datetime.fromtimestamp(unixTime, tz=datetime.timezone.utc)

    return Record(station, time), offset + recordFormatSize


def deserializeScan(buffer, offset=0):
    record, offset = deserializeRecord(buffer, offset)

    (
        elevationSize,
        azimuthSize,
        rangesSize,
        reflectivitySize,
        velocitySize,
    ) = struct.unpack_from(scanFormat, buffer, offset)

    offset += scanFormatSize

    elevations, offset = deserializeArray(buffer, offset, elevationSize)
    azimuths, offset = deserializeArray(buffer, offset, azimuthSize)
    ranges, offset = deserializeArray(buffer, offset, rangesSize)
    reflectivity, offset = deserializeArray(buffer, offset, reflectivitySize)
    velocity, offset = deserializeArray(buffer, offset, velocitySize)

    shape = (len(elevations), len(azimuths), len(ranges))
    reflectivity = reflectivity.reshape(shape)
    velocity = velocity.reshape(shape)

    return Scan(record, elevations, azimuths, ranges, reflectivity, velocity), offset


def deserializeArray(buffer, offset, size):
    return np.frombuffer(buffer[offset : offset + size]), offset + size
