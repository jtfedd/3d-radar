import datetime
import struct
from typing import Tuple

import numpy as np
import numpy.typing as npt

from lib.model.record import Record
from lib.model.scan import Scan

RECORD_FORMAT = "<d4s"
SCAN_FORMAT = "<5I"
RECORD_FORMAT_SIZE = struct.calcsize(RECORD_FORMAT)
SCAN_FORMAT_SIZE = struct.calcsize(SCAN_FORMAT)


def serializeScan(scan: Scan) -> bytes:
    buffer = serializeRecord(scan.record)

    elevationBytes = scan.elevations.tobytes()
    azimuthBytes = scan.azimuths.tobytes()
    rangesBytes = scan.ranges.tobytes()
    reflectivityBytes = scan.reflectivity.tobytes()
    velocityBytes = scan.velocity.tobytes()

    buffer += struct.pack(
        SCAN_FORMAT,
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


def serializeRecord(record: Record) -> bytes:
    return struct.pack(
        RECORD_FORMAT,
        int(record.time.timestamp()),
        bytes(record.station, "utf-8"),
    )


def deserializeRecord(buffer: bytes, offset: int = 0) -> Tuple[Record, int]:
    unixTime, stationBytes = struct.unpack_from(RECORD_FORMAT, buffer, offset=offset)
    station = stationBytes.rstrip(b"\x00").decode("utf-8")
    time = datetime.datetime.fromtimestamp(unixTime, tz=datetime.timezone.utc)

    return Record(station, time), offset + RECORD_FORMAT_SIZE


def deserializeScan(buffer: bytes, offset: int = 0) -> Tuple[Scan, int]:
    record, offset = deserializeRecord(buffer, offset)

    (
        elevationSize,
        azimuthSize,
        rangesSize,
        reflectivitySize,
        velocitySize,
    ) = struct.unpack_from(SCAN_FORMAT, buffer, offset)

    offset += SCAN_FORMAT_SIZE

    elevations, offset = deserializeArray(buffer, offset, elevationSize)
    azimuths, offset = deserializeArray(buffer, offset, azimuthSize)
    ranges, offset = deserializeArray(buffer, offset, rangesSize)
    reflectivity, offset = deserializeArray(buffer, offset, reflectivitySize)
    velocity, offset = deserializeArray(buffer, offset, velocitySize)

    shape = (len(elevations), len(azimuths), len(ranges))
    reflectivity = reflectivity.reshape(shape)
    velocity = velocity.reshape(shape)

    return Scan(record, elevations, azimuths, ranges, reflectivity, velocity), offset


def deserializeArray(
    buffer: bytes, offset: int, size: int
) -> Tuple[npt.NDArray[np.float32], int]:
    return (
        np.frombuffer(buffer[offset : offset + size], dtype=np.float32),
        offset + size,
    )
