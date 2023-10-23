import re

from panda3d.core import Vec4

from lib.util.errors import StateError


class UIColors:
    white = Vec4(1, 1, 1, 1)

    colorStringRegex = re.compile("^#[A-Fa-f0-9]{6}$")

    @staticmethod
    def fromHex(hexColor: str) -> Vec4:
        if UIColors.colorStringRegex.match(hexColor) is None:
            raise StateError("Invalid color " + hexColor)

        r = int(hexColor[1:3], 16) / 255.0
        g = int(hexColor[3:5], 16) / 255.0
        b = int(hexColor[5:7], 16) / 255.0

        return Vec4(r, g, b, 1)
