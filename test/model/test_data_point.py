from src.model.data_point import DataPoint

import random

import unittest

class TestDataPoint(unittest.TestCase):
    def test_serialize(self):
        input = DataPoint(1, 2, 3, 10)
        bytes = input.serialize()
        output = DataPoint.deserialize(bytes)

        self.assertEqual(input, output)

    def test_serialize_floats(self):
        input = DataPoint(1.1112, 2.32123, 42, 0.111222229)
        bytes = input.serialize()
        output = DataPoint.deserialize(bytes)

        self.assertEqual(input, output)

    def test_serialize_offset(self):
        input = DataPoint(1, 2, 3, 10)
        buffer = bytearray(random.randbytes(100))
        offset = 21

        writeOffset = input.writeBytes(buffer, offset)
        output, readOffset = input.fromSerial(buffer, offset)

        self.assertEqual(input, output)
        self.assertEqual(writeOffset, readOffset)
