import datetime
import struct
from typing import Tuple

from lib.model.record import Record
from lib.model.scan import Scan
from lib.model.scan_data import ScanData
from lib.model.sweep_meta import SweepMeta

SERIALIZATION_VERSION = 1

SWEEPMETA_FORMAT = "<5f5I"
SWEEPMETA_FORMAT_SIZE = struct.calcsize(SWEEPMETA_FORMAT)


def serializeScan(scan: Scan) -> bytes:
    buffer = serializeRecord(scan.record)
    buffer += serializeScanData(scan.reflectivity)
    buffer += serializeScanData(scan.velocity)
    return buffer


def deserializeScan(buffer: bytes, offset: int) -> Tuple[Scan, int]:
    record, offset = deserializeRecord(buffer, offset)
    reflectivity, offset = deserializeScanData(buffer, offset)
    velocity, offset = deserializeScanData(buffer, offset)
    return Scan(record, reflectivity=reflectivity, velocity=velocity), offset


def serializeScanData(scanData: ScanData) -> bytes:
    buffer = struct.pack("<I", len(scanData.metas))
    for meta in scanData.metas:
        buffer += serializeSweepMeta(meta)
    buffer += serializeBytes(scanData.data)
    return buffer


def deserializeScanData(buffer: bytes, offset: int) -> Tuple[ScanData, int]:
    length = int(struct.unpack_from("<I", buffer, offset=offset)[0])
    offset += struct.calcsize("<I")

    metas = []
    for _ in range(length):
        meta, offset = deserializeSweepMeta(buffer, offset)
        metas.append(meta)

    data, offset = deserializeBytes(buffer, offset)

    return ScanData(metas, data), offset


def serializeSweepMeta(meta: SweepMeta) -> bytes:
    return struct.pack(
        SWEEPMETA_FORMAT,
        meta.elevation,
        meta.azFirst,
        meta.azStep,
        meta.rngFirst,
        meta.rngStep,
        meta.azCount,
        meta.rngCount,
        int(round(meta.startTime.timestamp())),
        int(round(meta.endTime.timestamp())),
        meta.offset,
    )


def deserializeSweepMeta(buffer: bytes, buffOffset: int) -> Tuple[SweepMeta, int]:
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
        offset,
    ) = struct.unpack_from(SWEEPMETA_FORMAT, buffer, offset=buffOffset)

    return (
        SweepMeta(
            elevation=elevation,
            azFirst=azFirst,
            azStep=azStep,
            azCount=azCount,
            rngFirst=rngFirst,
            rngStep=rngStep,
            rngCount=rngCount,
            startTime=startTime,
            endTime=endTime,
            offset=offset,
        ),
        buffOffset + SWEEPMETA_FORMAT_SIZE,
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
