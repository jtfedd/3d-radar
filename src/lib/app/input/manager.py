from direct.showbase.DirectObject import DirectObject
from direct.showbase.ShowBase import ShowBase
from direct.task.Task import Task
from panda3d.core import MouseButton

from lib.app.focus.manager import FocusManager
from lib.app.state import AppState
from lib.util.events.event_dispatcher import EventDispatcher
from lib.util.events.listener import Listener

from .events import InputEvents


class InputManager(DirectObject):
    def __init__(
        self,
        base: ShowBase,
        focusManager: FocusManager,
        state: AppState,
        events: InputEvents,
    ):
        self.base = base
        self.focusManager = focusManager
        self.events = events
        self.state = state

        self.createBindings()

        self.listener = Listener()
        self.listener.listen(self.state.hideKeybinding, lambda _: self.createBindings())
        self.listener.listen(self.state.playKeybinding, lambda _: self.createBindings())
        self.listener.listen(self.state.nextKeybinding, lambda _: self.createBindings())
        self.listener.listen(self.state.prevKeybinding, lambda _: self.createBindings())

        self.mouse1Pressed = False
        self.mouse3Pressed = False
        self.updateTask = base.taskMgr.add(self.update, "input-update")

    def update(self, task: Task) -> int:
        mouse1pressed = self.base.mouseWatcherNode.isButtonDown(MouseButton.one())
        if mouse1pressed is not self.mouse1Pressed:
            self.mouse1Pressed = mouse1pressed
            self.events.leftMouseRaw.send(mouse1pressed)

        mouse3pressed = self.base.mouseWatcherNode.isButtonDown(MouseButton.three())
        if mouse3pressed is not self.mouse3Pressed:
            self.mouse3Pressed = mouse3pressed
            self.events.rightMouseRaw.send(mouse3pressed)

        return task.cont

    def createBindings(self) -> None:
        self.ignoreAll()

        self.accept(
            self.state.hideKeybinding.value, lambda: self.send(self.events.onHide)
        )

        self.accept(
            self.state.playKeybinding.value, lambda: self.send(self.events.onPlay)
        )

        self.accept(
            self.state.nextKeybinding.value, lambda: self.send(self.events.nextFrame)
        )

        self.accept(
            self.state.prevKeybinding.value, lambda: self.send(self.events.prevFrame)
        )

        self.accept(
            self.state.stationsButtonKeybinding.value,
            lambda: self.send(self.events.showStationsButtons),
        )
        self.accept(
            self.state.stationsButtonKeybinding.value + "-up",
            lambda: self.events.hideStationsButtons.send(None),
        )

        self.accept("wheel_up-up", lambda: self.events.scroll.send(-1))
        self.accept("wheel_down-up", lambda: self.events.scroll.send(1))

        self.accept("wheel_up", lambda: self.events.zoom.send(-1))
        self.accept("wheel_down", lambda: self.events.zoom.send(1))

        self.accept("mouse1", lambda: self.events.leftMouse.send(True))
        self.accept("mouse1-up", lambda: self.events.leftMouse.send(False))

        self.accept("mouse3", lambda: self.events.rightMouse.send(True))
        self.accept("mouse3-up", lambda: self.events.rightMouse.send(False))

        self.accept("tab", lambda: self.events.tab.send(True))
        self.accept("shift-tab", lambda: self.events.shiftTab.send(True))

    def send(self, event: EventDispatcher[None]) -> None:
        if self.focusManager.focused():
            return

        event.send(None)

    def destroy(self) -> None:
        self.ignoreAll()

        self.updateTask.cancel()
