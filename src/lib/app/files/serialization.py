import datetime
import struct
from typing import Tuple

from lib.model.record import Record
from lib.model.scan import Scan
from lib.model.sweep import Sweep

SERIALIZATION_VERSION = 2

SWEEP_FORMAT = "<5f4I"
SWEEP_FORMAT_SIZE = struct.calcsize(SWEEP_FORMAT)


def serializeScan(scan: Scan) -> bytes:
    buffer = serializeRecord(scan.record)
    buffer += struct.pack("<2I", len(scan.reflectivity), len(scan.velocity))
    for sweep in scan.reflectivity:
        buffer += serializeSweep(sweep)
    for sweep in scan.velocity:
        buffer += serializeSweep(sweep)
    return buffer


def deserializeScan(buffer: bytes, offset: int) -> Tuple[Scan, int]:
    record, offset = deserializeRecord(buffer, offset)
    reflectivitySweeps, velocitySweeps = struct.unpack_from("<2I", buffer, offset)
    offset += struct.calcsize("<2I")

    reflectivity = []
    velocity = []

    for _ in range(reflectivitySweeps):
        sweep, offset = deserializeSweep(buffer, offset)
        reflectivity.append(sweep)

    for _ in range(velocitySweeps):
        sweep, offset = deserializeSweep(buffer, offset)
        velocity.append(sweep)

    return Scan(record, reflectivity=reflectivity, velocity=velocity), offset


def serializeSweep(sweep: Sweep) -> bytes:
    buffer = struct.pack(
        SWEEP_FORMAT,
        sweep.elevation,
        sweep.azFirst,
        sweep.azStep,
        sweep.rngFirst,
        sweep.rngStep,
        sweep.azCount,
        sweep.rngCount,
        sweep.startTime,
        sweep.endTime,
    )

    buffer += serializeBytes(sweep.data)

    return buffer


def deserializeSweep(buffer: bytes, offset: int) -> Tuple[Sweep, int]:
    (
        elevation,
        azFirst,
        azStep,
        rngFirst,
        rngStep,
        azCount,
        rngCount,
        startTime,
        endTime,
    ) = struct.unpack_from(SWEEP_FORMAT, buffer, offset=offset)
    offset += SWEEP_FORMAT_SIZE

    data, offset = deserializeBytes(buffer, offset)

    return (
        Sweep(
            elevation=elevation,
            azFirst=azFirst,
            azStep=azStep,
            azCount=azCount,
            rngFirst=rngFirst,
            rngStep=rngStep,
            rngCount=rngCount,
            startTime=startTime,
            endTime=endTime,
            data=data,
        ),
        offset,
    )


def serializeRecord(record: Record) -> bytes:
    buffer = struct.pack(
        "<I",
        int(record.time.timestamp()),
    )

    buffer += serializeString(record.station)
    buffer += serializeString(record.extension)

    return buffer


def deserializeRecord(buffer: bytes, offset: int = 0) -> Tuple[Record, int]:
    unixTime = struct.unpack_from("<I", buffer, offset=offset)[0]
    offset += struct.calcsize("<I")
    station, offset = deserializeString(buffer, offset)
    extension, offset = deserializeString(buffer, offset)
    time = datetime.datetime.fromtimestamp(
        unixTime,
        tz=datetime.timezone.utc,
    )

    return Record(station, time, extension=extension), offset


def serializeString(s: str) -> bytes:
    sBytes = bytes(s, "utf-8")
    return struct.pack(f"<I{len(sBytes)}s", len(sBytes), sBytes)


def deserializeString(buffer: bytes, offset: int) -> Tuple[str, int]:
    length = int(struct.unpack_from("<I", buffer, offset=offset)[0])
    offset += struct.calcsize("<I")
    sBytes = struct.unpack_from(f"<{length}s", buffer, offset=offset)[0]
    offset += length

    return sBytes.rstrip(b"\x00").decode("utf-8"), offset


def serializeBytes(b: bytes) -> bytes:
    return struct.pack("<I", len(b)) + b


def deserializeBytes(buffer: bytes, offset: int) -> Tuple[bytes, int]:
    length = int(struct.unpack_from("<I", buffer, offset=offset)[0])
    offset += struct.calcsize("<I")
    b = buffer[offset : offset + length]
    offset += length
    return b, offset
