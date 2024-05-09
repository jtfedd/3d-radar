import unittest

from panda3d.core import Vec3, Vec4

from lib.ui.core.colors import fromHex, withAlpha
from lib.util.errors import StateError


class TestColors(unittest.TestCase):
    def testParseHexColor(self) -> None:
        self.assertEqual(fromHex("#000000"), Vec4(0, 0, 0, 1))
        self.assertEqual(fromHex("#FFFFFF"), Vec4(1, 1, 1, 1))

        self.assertEqual(withAlpha(fromHex("#000000"), 0.5), Vec4(0, 0, 0, 0.5))
        self.assertEqual(withAlpha(fromHex("#FFFFFF"), 0.75), Vec4(1, 1, 1, 0.75))

    def testParseHexColorInvalid(self) -> None:
        self.assertRaises(StateError, fromHex, "")
        self.assertRaises(StateError, fromHex, "#")
        self.assertRaises(StateError, fromHex, "#FFF")
        self.assertRaises(StateError, fromHex, "#FFFFF")
        self.assertRaises(StateError, fromHex, "#FFFFFFF")
        self.assertRaises(StateError, fromHex, "FFFFFF")
        self.assertRaises(StateError, fromHex, "#ABCDEG")
        self.assertRaises(StateError, fromHex, "#fFfffF")
