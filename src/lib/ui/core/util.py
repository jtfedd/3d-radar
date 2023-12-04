from panda3d.core import DynamicTextFont, TextNode

from lib.ui.core.alignment import HAlign, VAlign
from lib.util.errors import InvalidArgumentException


def correctXForAlignment(x: float, width: float, align: HAlign) -> float:
    offset = width / 2

    if align == HAlign.CENTER:
        return x

    if align == HAlign.LEFT:
        return x + offset

    if align == HAlign.RIGHT:
        return x - offset

    raise InvalidArgumentException("align has invalid value " + align.value)


def correctYForAlignment(y: float, height: float, align: VAlign) -> float:
    offset = height / 2

    if align == VAlign.CENTER:
        return y

    if align == VAlign.TOP:
        return y - offset

    if align in (VAlign.BOTTOM, VAlign.BASELINE):
        return y + offset

    raise InvalidArgumentException("align has invalid value " + align.value)


def horizontalAlignToTextNodeAlign(align: HAlign) -> int:
    if align == HAlign.LEFT:
        return TextNode.ALeft

    if align == HAlign.CENTER:
        return TextNode.ACenter

    if align == HAlign.RIGHT:
        return TextNode.ARight

    raise InvalidArgumentException("align has invalid value " + align.value)


def correctYForTextAlignment(
    y: float,
    font: DynamicTextFont,
    textSize: float,
    align: VAlign,
) -> float:
    if align == VAlign.BASELINE:
        return y

    if align == VAlign.TOP:
        return y - textSize

    if align == VAlign.CENTER:
        return y - textSize / 3.5

    if align == VAlign.BOTTOM:
        return y + textSize * (font.line_height - 1)

    raise InvalidArgumentException("align has invalid value " + align.value)


def getBaseline(font: DynamicTextFont, size: float) -> float:
    return (font.line_height - 1) * size
