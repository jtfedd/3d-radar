from src.model.scan import Scan
from test.testutils.models import newTestScan, randomBytes

import unittest


class TestScan(unittest.TestCase):
    def test_serialize(self):
        input = newTestScan()
        bytes = input.serialize()
        output = Scan.deserialize(bytes)

        self.assertEqual(input, output)

    def test_serialize_offset(self):
        input = newTestScan()
        buffer = randomBytes(50000)
        offset = 123

        writeOffset = input.writeBytes(buffer, offset)
        output, readOffset = Scan.fromSerial(buffer, offset)

        self.assertEqual(input, output)
        self.assertEqual(writeOffset, readOffset)
        self.assertNotEqual(offset, writeOffset)
        self.assertEqual(writeOffset - offset, input.byteSize())
