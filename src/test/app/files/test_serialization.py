import datetime
import random
import unittest
from test.testutils.models import (
    assertScansEqual,
    assertSweepsEqual,
    newTestScan,
    newTestSweep,
)

from lib.app.files import serialization
from lib.model.record import Record


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

    def testSerializeSweep(self) -> None:
        sweep = newTestSweep()

        b = serialization.serializeSweep(sweep)
        newSweep, offset = serialization.deserializeSweep(b, 0)

        self.assertEqual(offset, len(b))
        self.assertEqual(offset, 1040)

        assertSweepsEqual(self, sweep, newSweep)

    def testSerializeScan(self) -> None:
        scan = newTestScan()

        b = serialization.serializeScan(scan)
        newScan, offset = serialization.deserializeScan(b, 0)

        self.assertEqual(offset, len(b))
        self.assertEqual(offset, 20827)

        assertScansEqual(self, scan, newScan)
