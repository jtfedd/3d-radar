from src.model.reflectivity_header import ReflectivityHeader
from test.model.testutils import newTestReflectivityHeader, randomBytes

import unittest

class TestDataPoint(unittest.TestCase):
    def test_serialize(self):
        input = newTestReflectivityHeader()
        bytes = input.serialize()
        output = ReflectivityHeader.deserialize(bytes)

        self.assertEqual(input, output)

    def test_serialize_offset(self):
        input = newTestReflectivityHeader()
        buffer = randomBytes(100)
        offset = 42

        writeOffset = input.writeBytes(buffer, offset)
        output, readOffset = ReflectivityHeader.fromSerial(buffer, offset)

        self.assertEqual(input, output)
        self.assertEqual(writeOffset, readOffset)
        self.assertNotEqual(offset, writeOffset)
        self.assertEqual(writeOffset - offset, input.byteSize())
