import datetime
import random
import unittest

from lib.model.record import Record
from lib.model.scan import Scan
from lib.model.sweep import Sweep


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


def newTestSweep() -> Sweep:
    return Sweep(
        random.random(),
        random.random(),
        random.random(),
        random.randint(0, 1000),
        random.random(),
        random.random(),
        random.randint(0, 1000),
        random.randint(0, 100000),
        random.randint(0, 100000),
        random.randbytes(1000),
    )


def newTestScan() -> Scan:
    record = newTestRecord()
    reflectivity = [newTestSweep() for _ in range(10)]
    velocity = [newTestSweep() for _ in range(10)]

    return Scan(record, reflectivity, velocity)


def assertRecordsEqual(t: unittest.TestCase, first: Record, second: Record) -> None:
    t.assertIsInstance(first, Record)
    t.assertIsInstance(second, Record)

    t.assertEqual(first.station, second.station)
    t.assertEqual(first.time, second.time)


def assertSweepsEqual(t: unittest.TestCase, first: Sweep, second: Sweep) -> None:
    t.assertIsInstance(first, Sweep)
    t.assertIsInstance(second, Sweep)

    t.assertAlmostEqual(first.elevation, second.elevation)
    t.assertAlmostEqual(first.azFirst, second.azFirst)
    t.assertEqual(first.azCount, second.azCount)
    t.assertAlmostEqual(first.azStep, second.azStep)
    t.assertAlmostEqual(first.rngFirst, second.rngFirst)
    t.assertEqual(first.rngCount, second.rngCount)
    t.assertAlmostEqual(first.rngStep, second.rngStep)
    t.assertEqual(first.data, second.data)


def assertScansEqual(t: unittest.TestCase, first: Scan, second: Scan) -> None:
    t.assertIsInstance(first, Scan)
    t.assertIsInstance(second, Scan)

    assertRecordsEqual(t, first.record, second.record)

    t.assertEqual(len(first.reflectivity), len(second.reflectivity))
    for i, sweep in enumerate(first.reflectivity):
        assertSweepsEqual(t, sweep, second.reflectivity[i])

    t.assertEqual(len(first.velocity), len(second.velocity))
    for i, sweep in enumerate(first.velocity):
        assertSweepsEqual(t, sweep, second.velocity[i])
