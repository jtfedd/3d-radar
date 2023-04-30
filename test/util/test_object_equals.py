from src.util.object_equals import ObjectEquals

import unittest


class TestObject(ObjectEquals):
    def __init__(self, x):
        self.x = x


class TestObjectEquals(unittest.TestCase):
    def test_objectEquals(self):
        a = TestObject(1)
        b = TestObject(1)
        c = TestObject(2)

        self.assertEqual(a, b)
        self.assertEqual(b, a)
        self.assertNotEqual(a, c)
        self.assertNotEqual(c, a)
        self.assertNotEqual(b, c)
        self.assertNotEqual(c, b)
