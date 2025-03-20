from enum import Enum
from typing import Dict

from direct.directnotify.DirectNotify import DirectNotify
from direct.directnotify.Notifier import Notifier
from panda3d.core import loadPrcFileData


class LoggingLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LoggingManager:
    def __init__(self) -> None:
        self.loggers: Dict[str, Notifier] = {}

    def newLogger(self, name: str) -> Notifier:
        logger = DirectNotify().newCategory(name)
        self.loggers[name] = logger
        return logger

    def setLevel(self, name: str, level: LoggingLevel) -> None:
        loadPrcFileData("", f"notify-category-{name} {level}")
