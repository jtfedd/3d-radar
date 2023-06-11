import datetime
import unittest

import numpy as np
import numpy.typing as npt

from lib.model.record import Record
from lib.model.scan import Scan


def newTestRecord() -> Record:
    time = datetime.datetime(
        2020,
        10,
        20,
        hour=1,
        minute=10,
        second=42,
        tzinfo=datetime.timezone.utc,
    )

    return Record("KDMX", time)


def newTestScan() -> Scan:
    record = newTestRecord()
    elevations = np.random.uniform(low=0, high=100, size=10).astype(np.float32)
    azimuths = np.random.uniform(low=0, high=100, size=100).astype(np.float32)
    ranges = np.random.uniform(low=0, high=100, size=1000).astype(np.float32)
    reflectivity = np.random.uniform(low=-25, high=75, size=(10, 100, 1000)).astype(
        np.float32
    )
    velocity = np.random.uniform(low=-100, high=100, size=(10, 100, 1000)).astype(
        np.float32
    )
    return Scan(record, elevations, azimuths, ranges, reflectivity, velocity)


def assertRecordsEqual(t: unittest.TestCase, first: Record, second: Record) -> None:
    t.assertIsInstance(first, Record)
    t.assertIsInstance(second, Record)

    t.assertEqual(first.station, second.station)
    t.assertEqual(first.time, second.time)


def assertScansEqual(t: unittest.TestCase, first: Scan, second: Scan) -> None:
    t.assertIsInstance(first, Scan)
    t.assertIsInstance(second, Scan)

    assertRecordsEqual(t, first.record, second.record)

    assertArraysAlmostEqual(t, first.elevations, second.elevations)
    assertArraysAlmostEqual(t, first.azimuths, second.azimuths)
    assertArraysAlmostEqual(t, first.ranges, second.ranges)
    assertArraysAlmostEqual(t, first.reflectivity, second.reflectivity)
    assertArraysAlmostEqual(t, first.velocity, second.velocity)


def assertArraysAlmostEqual(
    t: unittest.TestCase,
    first: npt.NDArray[np.float32],
    second: npt.NDArray[np.float32],
) -> None:
    t.assertEqual(first.shape, second.shape)

    elements = len(first)

    if len(first.shape) > 1:
        for i in range(elements):
            assertArraysAlmostEqual(t, first[i], second[i])
        return

    for i in range(elements):
        t.assertAlmostEqual(first[i], second[i])
