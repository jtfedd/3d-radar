import re

from panda3d.core import Vec4

from lib.util.errors import StateError


def fromHexWithAlpha(hexColor: str, alpha: float) -> Vec4:
    colorStringRegex = re.compile("^#[A-F0-9]{6}$")

    if colorStringRegex.match(hexColor) is None:
        raise StateError("Invalid color " + hexColor)

    r = int(hexColor[1:3], 16) / 255.0
    g = int(hexColor[3:5], 16) / 255.0
    b = int(hexColor[5:7], 16) / 255.0

    return Vec4(r, g, b, alpha)


def fromHex(hexColor: str) -> Vec4:
    return fromHexWithAlpha(hexColor, 1)


class UIColors:
    # Palette colors, dark to light
    PALETTE_0 = fromHex("#212529")  # Inset, depressed
    PALETTE_1 = fromHex("#343A40")  # Background, Content Dark
    PALETTE_2 = fromHex("#495057")  # Lighter button
    PALETTE_3 = fromHex("#6C757D")  # Hover dark
    PALETTE_4 = fromHex("#ADB5BD")
    PALETTE_5 = fromHex("#CED4DA")  # Slider bar, depressed light
    PALETTE_6 = fromHex("#DEE2E6")
    PALETTE_7 = fromHex("#E9ECEF")  # Content Light, light button
    PALETTE_8 = fromHex("#F8F9FA")  # Hover light

    # Generic colors
    TRANSPARENT = fromHexWithAlpha("#000000", 0)
    WHITE = fromHex("#FFFFFF")
    GRAY_0 = fromHex("#595959")
    GRAY_1 = fromHex("#7F7F7F")
    GRAY_2 = fromHex("#A5A5A5")
    GRAY_3 = fromHex("#CCCCCC")
    GRAY_4 = fromHex("#F2F2F2")
    BLACK = fromHex("#000000")

    # Special colors
    RED = fromHex("#E5383B")
    ORANGE = fromHex("#FCA311")

    # Role colors
    INSET = PALETTE_0

    BACKGROUND = PALETTE_1
    CONTENT = PALETTE_8
    HOVER = PALETTE_2
    DEPRESSED = PALETTE_0
    BACKGROUND_DISABLED = GRAY_0
    CONTENT_DISABLED = GRAY_3

    ACCENT = PALETTE_2
    ACCENT_HOVER = PALETTE_3
    BACKGROUND_DISABLED_ACCENT = GRAY_1

    BACKGROUND_LIGHT = PALETTE_8
    CONTENT_LIGHT = PALETTE_1
    HOVER_LIGHT = PALETTE_8
    DEPRESSED_LIGHT = PALETTE_5
    BACKGROUND_DISABLED_LIGHT = GRAY_3
    CONTENT_DISABLED_LIGHT = GRAY_0

    SLIDER_BAR = PALETTE_3
    SLIDER_THUMB = PALETTE_8
