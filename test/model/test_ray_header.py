from src.model.ray_header import RayHeader
from test.model.testutils import newTestRayHeader, randomBytes

import unittest

class TestDataPoint(unittest.TestCase):
    def test_serialize(self):
        input = newTestRayHeader(elevation=1.223344)
        bytes = input.serialize()
        output = RayHeader.deserialize(bytes)

        self.assertEqual(input, output)

    def test_serialize_offset(self):
        input = newTestRayHeader(azimuth=123.456789)
        buffer = randomBytes(100)
        offset = 42

        writeOffset = input.writeBytes(buffer, offset)
        output, readOffset = RayHeader.fromSerial(buffer, offset)

        self.assertEqual(input, output)
        self.assertEqual(writeOffset, readOffset)
        self.assertNotEqual(offset, writeOffset)
        self.assertEqual(writeOffset - offset, input.byteSize())
