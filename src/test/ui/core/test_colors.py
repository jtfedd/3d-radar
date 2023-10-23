import unittest

from panda3d.core import Vec4

from lib.ui.core.colors import UIColors
from lib.util.errors import StateError


class TestColors(unittest.TestCase):
    def testParseHexColor(self) -> None:
        self.assertEqual(UIColors.fromHex("#000000"), Vec4(0, 0, 0, 1))
        self.assertEqual(UIColors.fromHex("#FFFFFF"), Vec4(1, 1, 1, 1))

    def testParseHexColorInvalid(self) -> None:
        self.assertRaises(StateError, UIColors.fromHex, "")
        self.assertRaises(StateError, UIColors.fromHex, "#")
        self.assertRaises(StateError, UIColors.fromHex, "#FFF")
        self.assertRaises(StateError, UIColors.fromHex, "#FFFFF")
        self.assertRaises(StateError, UIColors.fromHex, "#FFFFFFF")
        self.assertRaises(StateError, UIColors.fromHex, "FFFFFF")
        self.assertRaises(StateError, UIColors.fromHex, "#ABCDEG")
        self.assertRaises(StateError, UIColors.fromHex, "#fFfffF")
