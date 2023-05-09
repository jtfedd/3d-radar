from model.scan import Scan
from model.sweep import Sweep
from model.ray import Ray
import struct
import datetime
import numpy as np

scanFormat = "<H6B4s"
sweepFormat = "<H"
rayFormat = "<4dI"
scanFormatBytes = struct.calcsize(scanFormat)
sweepFormatBytes = struct.calcsize(sweepFormat)
rayFormatBytes = struct.calcsize(rayFormat)


def serializeScan(scan):
    buffer = struct.pack(
        scanFormat,
        scan.date.year,
        scan.date.month,
        scan.date.day,
        scan.time.hour,
        scan.time.minute,
        scan.time.second,
        len(scan.sweeps),
        bytes(scan.station, "utf-8"),
    )
    for sweep in scan.sweeps:
        buffer += serializeSweep(sweep)

    return buffer


def serializeSweep(sweep):
    buffer = struct.pack(sweepFormat, len(sweep.rays))
    for ray in sweep.rays:
        buffer += serializeRay(ray)
    return buffer


def serializeRay(ray):
    refBytes = ray.reflectivity.tobytes()
    buffer = struct.pack(
        rayFormat,
        ray.azimuth,
        ray.elevation,
        ray.first,
        ray.spacing,
        len(refBytes),
    )
    buffer += refBytes
    return buffer


def deserializeScan(buffer, offset=0):
    (
        year,
        month,
        day,
        hour,
        minute,
        second,
        numSweeps,
        stationBytes,
    ) = struct.unpack_from(scanFormat, buffer, offset)
    offset += scanFormatBytes

    station = stationBytes.rstrip(b"\x00").decode("utf_8")
    date = datetime.date(year=year, month=month, day=day)
    time = datetime.time(hour=hour, minute=minute, second=second)

    sweeps = []
    for _ in range(numSweeps):
        sweep, offset = deserializeSweep(buffer, offset)
        sweeps.append(sweep)

    return Scan(sweeps, station, date, time), offset


def deserializeSweep(buffer, offset=0):
    numRays = struct.unpack_from(sweepFormat, buffer, offset)[0]
    offset += sweepFormatBytes

    rays = []
    for _ in range(numRays):
        ray, offset = deserializeRay(buffer, offset)
        rays.append(ray)

    return Sweep(rays), offset


def deserializeRay(buffer, offset=0):
    (azimuth, elevation, first, spacing, numRefBytes) = struct.unpack_from(
        rayFormat, buffer, offset
    )
    offset += rayFormatBytes

    reflectivity = np.frombuffer(buffer[offset : offset + numRefBytes])
    offset += numRefBytes

    return Ray(azimuth, elevation, first, spacing, reflectivity), offset
