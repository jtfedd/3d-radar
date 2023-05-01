from src.model.sweep import Sweep
from test.testutils.models import newTestSweep, randomBytes

import unittest


class TestSweep(unittest.TestCase):
    def test_serialize(self):
        input = newTestSweep()
        bytes = input.serialize()
        output = Sweep.deserialize(bytes)

        self.assertEqual(input, output)

    def test_serialize_offset(self):
        input = newTestSweep()
        buffer = randomBytes(10000)
        offset = 123

        writeOffset = input.writeBytes(buffer, offset)
        output, readOffset = Sweep.fromSerial(buffer, offset)

        self.assertEqual(input, output)
        self.assertEqual(writeOffset, readOffset)
        self.assertNotEqual(offset, writeOffset)
        self.assertEqual(writeOffset - offset, input.byteSize())
