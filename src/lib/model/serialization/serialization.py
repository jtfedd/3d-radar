import datetime
import struct
from typing import Tuple

from lib.model.record import Record
from lib.model.scan import Scan
from lib.model.scan_data import ScanData
from lib.model.sweep_meta import SweepMeta

RECORD_FORMAT = "<d4s"
RECORD_FORMAT_SIZE = struct.calcsize(RECORD_FORMAT)
SCANDATA_FORMAT = "<2I"
SCANDATA_FORMAT_SIZE = struct.calcsize(SCANDATA_FORMAT)
SWEEPMETA_FORMAT = "<5f3I"
SWEEPMETA_FORMAT_SIZE = struct.calcsize(SWEEPMETA_FORMAT)


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
        meta.offset,
    )


def deserializeSweepMeta(buffer: bytes, bufOffset: int = 0) -> Tuple[SweepMeta, int]:
    (
        elevation,
        azFirst,
        azStep,
        rngFirst,
        rngStep,
        azCount,
        rngCount,
        offset,
    ) = struct.unpack_from(SWEEPMETA_FORMAT, buffer, offset=bufOffset)

    return (
        SweepMeta(
            elevation, azFirst, azStep, azCount, rngFirst, rngStep, rngCount, offset
        ),
        bufOffset + SWEEPMETA_FORMAT_SIZE,
    )


def serializeScanData(scan: ScanData) -> bytes:
    buffer = struct.pack(SCANDATA_FORMAT, len(scan.data), len(scan.metas))
    for meta in scan.metas:
        buffer += serializeSweepMeta(meta)
    buffer += scan.data

    return buffer


def deserializeScanData(buffer: bytes, offset: int = 0) -> Tuple[ScanData, int]:
    dataLen, metaLen = struct.unpack_from(SCANDATA_FORMAT, buffer, offset=offset)
    offset += SCANDATA_FORMAT_SIZE

    metas = []
    for _ in range(metaLen):
        meta, offset = deserializeSweepMeta(buffer, offset)
        metas.append(meta)

    data = buffer[offset : offset + dataLen]
    offset += dataLen

    return (ScanData(metas, data), offset)


def serializeScan(scan: Scan) -> bytes:
    buffer = serializeRecord(scan.record)
    buffer += serializeScanData(scan.reflectivity)
    buffer += serializeScanData(scan.velocity)

    return buffer


def deserializeScan(buffer: bytes, offset: int = 0) -> Tuple[Scan, int]:
    record, offset = deserializeRecord(buffer, offset)
    reflectivity, offset = deserializeScanData(buffer, offset)
    velocity, offset = deserializeScanData(buffer, offset)

    return Scan(record, reflectivity, velocity), offset


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
