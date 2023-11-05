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
