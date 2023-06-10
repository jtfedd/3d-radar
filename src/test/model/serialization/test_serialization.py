import unittest
from test.testutils.models import (
    assertRecordsEqual,
    assertScansEqual,
    newTestRecord,
    newTestScan,
)

from lib.model.serialization import serialization


class TestSerialization(unittest.TestCase):
    def testSerializeRecord(self) -> None:
        record = newTestRecord()
        recordBytes = serialization.serializeRecord(record)
        self.assertEqual(len(recordBytes), 12)

        output, size = serialization.deserializeRecord(recordBytes)
        assertRecordsEqual(self, record, output)
        self.assertEqual(size, len(recordBytes))

    def testSerializeScan(self) -> None:
        scan = newTestScan()
        scanBytes = serialization.serializeScan(scan)
        self.assertEqual(len(scanBytes), 16008912)

        output, size = serialization.deserializeScan(scanBytes)
        assertScansEqual(self, scan, output)
        self.assertEqual(size, len(scanBytes))
