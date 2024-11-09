from direct.directnotify.DirectNotify import DirectNotify
from direct.directnotify.Notifier import Notifier


def newLogger(name: str) -> Notifier:
    return DirectNotify().newCategory(name)
