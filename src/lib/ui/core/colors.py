import re

from panda3d.core import Vec4

from lib.util.errors import StateError


class UIColors:
    @staticmethod
    def fromHex(hexColor: str) -> Vec4:
        colorStringRegex = re.compile("^#[A-F0-9]{6}$")

        if colorStringRegex.match(hexColor) is None:
            raise StateError("Invalid color " + hexColor)

        r = int(hexColor[1:3], 16) / 255.0
        g = int(hexColor[3:5], 16) / 255.0
        b = int(hexColor[5:7], 16) / 255.0

        return Vec4(r, g, b, 1)

    WHTIE = fromHex("#FFFFFF")
    BLACK = fromHex("#000000")
    GRAY = fromHex("#454545")
