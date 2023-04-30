from src.model.data_point import DataPoint
from test.model.testutils import newTestDataPoint, randomBytes

import unittest

class TestDataPoint(unittest.TestCase):
    def test_serialize(self):
        input = newTestDataPoint(y=2.32112233, reflectivity=0.111222233339)
        bytes = input.serialize()
        output = DataPoint.deserialize(bytes)

        self.assertEqual(input, output)

    def test_serialize_offset(self):
        input = newTestDataPoint(y=2.32112233, reflectivity=0.111222233339)
        buffer = randomBytes(100)
        offset = 21

        writeOffset = input.writeBytes(buffer, offset)
        output, readOffset = DataPoint.fromSerial(buffer, offset)

        self.assertEqual(input, output)
        self.assertEqual(writeOffset, readOffset)
        self.assertNotEqual(offset, writeOffset)
        self.assertEqual(writeOffset - offset, input.byteSize())
