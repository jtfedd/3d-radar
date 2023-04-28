from src.model.data_point import DataPoint

import unittest

class TestDataPoint(unittest.TestCase):
    def test_serialize(self):
        input = DataPoint(1, 2, 3, 10)
        bytes = input.serialize()
        output = DataPoint.deserialize(bytes)

        self.assertEqual(input, output)
