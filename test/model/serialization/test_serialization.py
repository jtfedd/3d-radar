from src.model.serialization import serialization
from test.testutils.models import *
import unittest


class TestSerialization(unittest.TestCase):
    def test_serialize_ray(self):
        input = newTestRay()
        bytes = serialization.serializeRay(input)
        output, size = serialization.deserializeRay(bytes)

        assertRaysEqual(self, input, output)
        self.assertEqual(size, 116)

    def test_serialize_sweep(self):
        input = newTestSweep()
        bytes = serialization.serializeSweep(input)
        output, size = serialization.deserializeSweep(bytes)

        assertSweepsEqual(self, input, output)
        self.assertEqual(size, 1162)

    def test_serialize_scan(self):
        input = newTestScan()
        bytes = serialization.serializeScan(input)
        output, size = serialization.deserializeScan(bytes)

        assertScansEqual(self, input, output)
        self.assertEqual(size, 11632)
