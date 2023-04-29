from src.model.ray_header import RayHeader
import random

import unittest

class TestDataPoint(unittest.TestCase):
    def test_serialize(self):
        input = RayHeader(1, 2)
        bytes = input.serialize()
        output = RayHeader.deserialize(bytes)

        self.assertEqual(input, output)

    def test_serialize_floats(self):
        input = RayHeader(1.1112, 2.32123)
        bytes = input.serialize()
        output = RayHeader.deserialize(bytes)

        self.assertEqual(input, output)

    def test_serialize_offset(self):
        input = RayHeader(1, 2.32423)
        buffer = bytearray(random.randbytes(100))
        offset = 42

        writeOffset = input.writeBytes(buffer, offset)
        output, readOffset = input.fromSerial(buffer, offset)

        self.assertEqual(input, output)
        self.assertEqual(writeOffset, readOffset)
        self.assertNotEqual(offset, writeOffset)
