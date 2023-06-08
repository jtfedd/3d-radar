import datetime
import unittest

import numpy as np

from lib.model.record import Record
from lib.model.scan import Scan


def newTestRecord():
    time = datetime.datetime(
        2019,
        6,
        26,
        hour=22,
        minute=11,
        second=5,
        tzinfo=datetime.timezone.utc,
    )

    return Record("KDMX", time)


def newTestScan():
    record = newTestRecord()
    elevations = np.random.uniform(low=0, high=100, size=(10))
    azimuths = np.random.uniform(low=0, high=100, size=(100))
    ranges = np.random.uniform(low=0, high=100, size=(1000))
    reflectivity = np.random.uniform(low=-25, high=75, size=(10, 100, 1000))
    velocity = np.random.uniform(low=-100, high=100, size=(10, 100, 1000))
    return Scan(record, elevations, azimuths, ranges, reflectivity, velocity)


def assertRecordsEqual(t: unittest.TestCase, first: Record, second: Record):
    t.assertIsInstance(first, Record)
    t.assertIsInstance(second, Record)

    t.assertEqual(first.station, second.station)
    t.assertEqual(first.time, second.time)


def assertScansEqual(t: unittest.TestCase, first: Scan, second: Scan):
    t.assertIsInstance(first, Scan)
    t.assertIsInstance(second, Scan)

    assertRecordsEqual(t, first.record, second.record)

    assertArraysAlmostEqual(t, first.elevations, second.elevations)
    assertArraysAlmostEqual(t, first.azimuths, second.azimuths)
    assertArraysAlmostEqual(t, first.ranges, second.ranges)
    assertArraysAlmostEqual(t, first.reflectivity, second.reflectivity)
    assertArraysAlmostEqual(t, first.velocity, second.velocity)


def assertArraysAlmostEqual(t: unittest.TestCase, first, second):
    t.assertEqual(first.shape, second.shape)

    if len(first.shape) > 1:
        for i in range(len(first)):
            assertArraysAlmostEqual(t, first[i], second[i])
        return

    for i in range(len(first)):
        t.assertAlmostEqual(first[i], second[i])
