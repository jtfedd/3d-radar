import datetime
import random
import unittest

from lib.app.files import serialization
from lib.model.record import Record
from lib.model.scan import Scan
from lib.model.scan_data import ScanData
from lib.model.sweep_meta import SweepMeta


def testSweepMeta() -> SweepMeta:
    return SweepMeta(
        elevation=random.random(),
        azFirst=random.random(),
        azStep=random.random(),
        azCount=random.randint(0, 100),
        rngFirst=random.random(),
        rngStep=random.random(),
        rngCount=random.randint(0, 100),
        startTime=random.randint(0, 100000),
        endTime=random.randint(0, 100000),
        offset=random.randint(0, 100),
    )


def assertSweepMetaEqual(t: unittest.TestCase, a: SweepMeta, b: SweepMeta) -> None:
    t.assertAlmostEqual(a.elevation, b.elevation)
    t.assertAlmostEqual(a.azFirst, b.azFirst)
    t.assertAlmostEqual(a.azStep, b.azStep)
    t.assertEqual(a.azCount, b.azCount)
    t.assertAlmostEqual(a.rngFirst, b.rngFirst)
    t.assertAlmostEqual(a.rngStep, b.rngStep)
    t.assertEqual(a.rngCount, b.rngCount)
    t.assertEqual(a.startTime, b.startTime)
    t.assertEqual(a.endTime, b.endTime)
    t.assertEqual(a.offset, b.offset)


def testScanData() -> ScanData:
    return ScanData([testSweepMeta() for _ in range(5)], random.randbytes(100))


def assertScanDataEqual(t: unittest.TestCase, a: ScanData, b: ScanData) -> None:
    t.assertEqual(len(a.metas), len(b.metas))
    for meta, newMeta in zip(a.metas, b.metas):
        assertSweepMetaEqual(t, meta, newMeta)

    t.assertEqual(a.data, b.data)


def testRecord() -> Record:
    return Record(
        "KABC",
        datetime.datetime.now(datetime.UTC),
        extension="QWERTY",
    )


def assertRecordEqual(t: unittest.TestCase, a: Record, b: Record) -> None:
    t.assertEqual(a.station, b.station)
    t.assertEqual(a.extension, b.extension)
    t.assertEqual(a.time.year, b.time.year)
    t.assertEqual(a.time.month, b.time.month)
    t.assertEqual(a.time.day, b.time.day)
    t.assertEqual(a.time.hour, b.time.hour)
    t.assertEqual(a.time.minute, b.time.minute)
    t.assertEqual(a.time.second, b.time.second)


class TestSerialization(unittest.TestCase):
    def testSerializeString(self) -> None:
        b = serialization.serializeString("asdf")
        s, offset = serialization.deserializeString(b, 0)

        self.assertEqual("asdf", s)
        self.assertEqual(offset, len(b))
        self.assertEqual(offset, 8)

    def testSerializeBytes(self) -> None:
        randomBytes = random.randbytes(100)
        b = serialization.serializeBytes(randomBytes)
        ub, offset = serialization.deserializeBytes(b, 0)

        self.assertEqual(randomBytes, ub)
        self.assertEqual(offset, len(b))
        self.assertEqual(offset, 104)

    def testSerializeRecord(self) -> None:
        record = testRecord()

        b = serialization.serializeRecord(record)
        newRecord, offset = serialization.deserializeRecord(b, 0)

        self.assertEqual(offset, len(b))
        self.assertEqual(offset, 22)

        assertRecordEqual(self, record, newRecord)

    def testSerializeSweepMeta(self) -> None:
        meta = testSweepMeta()

        b = serialization.serializeSweepMeta(meta)
        newMeta, offset = serialization.deserializeSweepMeta(b, 0)

        self.assertEqual(offset, len(b))
        self.assertEqual(offset, 40)

        assertSweepMetaEqual(self, meta, newMeta)

    def testSerializeScanData(self) -> None:
        data = testScanData()

        b = serialization.serializeScanData(data)
        newData, offset = serialization.deserializeScanData(b, 0)

        self.assertEqual(offset, len(b))
        self.assertEqual(offset, 308)

        assertScanDataEqual(self, data, newData)

    def testSerializeScan(self) -> None:
        scan = Scan(testRecord(), testScanData(), testScanData())

        b = serialization.serializeScan(scan)
        newScan, offset = serialization.deserializeScan(b, 0)

        self.assertEqual(offset, len(b))
        self.assertEqual(offset, 638)

        assertRecordEqual(self, scan.record, newScan.record)
        assertScanDataEqual(self, scan.reflectivity, newScan.reflectivity)
        assertScanDataEqual(self, scan.velocity, newScan.velocity)
