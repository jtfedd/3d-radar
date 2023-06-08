import unittest
from test.testutils.models import (
    assertRecordsEqual,
    assertScansEqual,
    newTestRecord,
    newTestScan,
)

from lib.model.serialization import serialization


class TestSerialization(unittest.TestCase):
    def test_serialize_record(self):
        input = newTestRecord()
        bytes = serialization.serializeRecord(input)
        self.assertEqual(len(bytes), 12)

        output, size = serialization.deserializeRecord(bytes)
        assertRecordsEqual(self, input, output)
        self.assertEqual(size, len(bytes))

    def test_serialize_scan(self):
        input = newTestScan()
        bytes = serialization.serializeScan(input)
        self.assertEqual(len(bytes), 16008912)

        output, size = serialization.deserializeScan(bytes)
        assertScansEqual(self, input, output)
        self.assertEqual(size, len(bytes))
