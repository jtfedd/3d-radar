from src.model.reflectivity_header import ReflectivityHeader
import random

import unittest

class TestDataPoint(unittest.TestCase):
    def test_serialize(self):
        input = ReflectivityHeader(17, 2, 3)
        bytes = input.serialize()
        output = ReflectivityHeader.deserialize(bytes)

        self.assertEqual(input, output)

    def test_serialize_floats(self):
        input = ReflectivityHeader(281, 2.32123, 5.12339)
        bytes = input.serialize()
        output = ReflectivityHeader.deserialize(bytes)

        self.assertEqual(input, output)

    def test_serialize_offset(self):
        input = ReflectivityHeader(422, 2.32423, 0.003333)
        buffer = bytearray(random.randbytes(100))
        offset = 42

        writeOffset = input.writeBytes(buffer, offset)
        output, readOffset = input.fromSerial(buffer, offset)

        self.assertEqual(input, output)
        self.assertEqual(writeOffset, readOffset)
        self.assertNotEqual(offset, writeOffset)
