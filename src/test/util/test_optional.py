import unittest

from lib.util.optional import unwrap


class TestObject:
    def __init__(self, x: int) -> None:
        self.x = x


class TestOptionalUtils(unittest.TestCase):
    def testUnwrapObject(self) -> None:
        string = "blah"
        number = 42
        obj = TestObject(1)

        self.assertEqual(unwrap(string), string)
        self.assertEqual(unwrap(number), number)
        self.assertEqual(unwrap(obj), obj)

    def testUnwrapNone(self) -> None:
        self.assertRaises(TypeError, lambda: unwrap(None))
