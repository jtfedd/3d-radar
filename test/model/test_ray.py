from src.model.ray import Ray
from test.model.testutils import newTestRay, randomBytes

import unittest

class TestDataPoint(unittest.TestCase):
    def test_serialize(self):
        input = newTestRay()
        bytes = input.serialize()
        output = Ray.deserialize(bytes)

        self.assertEqual(input, output)

    def test_serialize_offset(self):
        input = newTestRay()
        buffer = randomBytes(1000)
        offset = 42

        writeOffset = input.writeBytes(buffer, offset)
        output, readOffset = Ray.fromSerial(buffer, offset)

        self.assertEqual(input, output)
        self.assertEqual(writeOffset, readOffset)
        self.assertNotEqual(offset, writeOffset)
        self.assertEqual(writeOffset - offset, input.byteSize())
