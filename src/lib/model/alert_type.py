from enum import Enum

from lib.util.errors import InvalidArgumentException


class AlertType(Enum):
    TORNADO_WARNING = 0
    SEVERE_THUNDERSTORM_WARNING = 1

    def code(self) -> str:
        if self.value == AlertType.TORNADO_WARNING.value:
            return "TOW"
        if self.value == AlertType.SEVERE_THUNDERSTORM_WARNING.value:
            return "SVW"
        raise InvalidArgumentException("Unsupported value: " + str(self.value))
