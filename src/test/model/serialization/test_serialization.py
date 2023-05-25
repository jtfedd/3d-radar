from lib.model.serialization import serialization
from test.testutils.models import *
import unittest


class TestSerialization(unittest.TestCase):
    def test_serialize_ray(self):
        input = newTestRay()
        bytes = serialization.serializeRay(input)
        self.assertEqual(len(bytes), 108)

        output, size = serialization.deserializeRay(bytes)
        assertRaysEqual(self, input, output)
        self.assertEqual(size, len(bytes))

    def test_serialize_sweep(self):
        input = newTestSweep()
        bytes = serialization.serializeSweep(input)
        self.assertEqual(len(bytes), 1090)

        output, size = serialization.deserializeSweep(bytes)
        assertSweepsEqual(self, input, output)
        self.assertEqual(size, len(bytes))

    def test_serialize_scan(self):
        input = newTestScan()
        bytes = serialization.serializeScan(input)
        self.assertEqual(len(bytes), 10912)

        output, size = serialization.deserializeScan(bytes)
        assertScansEqual(self, input, output)
        self.assertEqual(size, len(bytes))
