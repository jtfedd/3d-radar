import datetime
import random
import unittest

from lib.model.record import Record
from lib.model.scan import Scan
from lib.model.scan_data import ScanData
from lib.model.sweep_meta import SweepMeta


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


def newTestSweepMeta() -> SweepMeta:
    return SweepMeta(
        random.random(),
        random.random(),
        random.random(),
        random.randint(0, 1000),
        random.random(),
        random.random(),
        random.randint(0, 1000),
        random.randint(0, 1000),
    )


def newTestScanData() -> ScanData:
    return ScanData(
        [newTestSweepMeta() for _ in range(10)],
        random.randbytes(1000),
    )


def newTestScan() -> Scan:
    record = newTestRecord()
    reflectivity = newTestScanData()
    velocity = newTestScanData()

    return Scan(record, reflectivity, velocity)


def assertRecordsEqual(t: unittest.TestCase, first: Record, second: Record) -> None:
    t.assertIsInstance(first, Record)
    t.assertIsInstance(second, Record)

    t.assertEqual(first.station, second.station)
    t.assertEqual(first.time, second.time)


def assertSweepMetasEqual(
    t: unittest.TestCase, first: SweepMeta, second: SweepMeta
) -> None:
    t.assertIsInstance(first, SweepMeta)
    t.assertIsInstance(second, SweepMeta)

    t.assertAlmostEqual(first.elevation, second.elevation)
    t.assertAlmostEqual(first.azFirst, second.azFirst)
    t.assertEqual(first.azCount, second.azCount)
    t.assertAlmostEqual(first.azStep, second.azStep)
    t.assertAlmostEqual(first.rngFirst, second.rngFirst)
    t.assertEqual(first.rngCount, second.rngCount)
    t.assertAlmostEqual(first.rngStep, second.rngStep)
    t.assertEqual(first.offset, second.offset)


def assertScanDatasEqual(
    t: unittest.TestCase, first: ScanData, second: ScanData
) -> None:
    t.assertIsInstance(first, ScanData)
    t.assertIsInstance(second, ScanData)

    t.assertEqual(len(first.metas), len(second.metas))
    for i, meta in enumerate(first.metas):
        assertSweepMetasEqual(t, meta, second.metas[i])

    t.assertEqual(first.data, second.data)


def assertScansEqual(t: unittest.TestCase, first: Scan, second: Scan) -> None:
    t.assertIsInstance(first, Scan)
    t.assertIsInstance(second, Scan)

    assertRecordsEqual(t, first.record, second.record)
    assertScanDatasEqual(t, first.reflectivity, second.reflectivity)
    assertScanDatasEqual(t, first.velocity, second.velocity)
