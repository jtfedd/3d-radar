from direct.showbase.ShowBase import ShowBase
from panda3d.core import GraphicsWindow

from lib.app.window.events import WindowEvents
from lib.util.events.listener import Listener


class ResolutionProvider(Listener):
    def __init__(self, base: ShowBase, events: WindowEvents):
        super().__init__()

        self.base = base

        # For some reason this seems to be typed incorrectly; override the type
        window: GraphicsWindow = base.win  # type: ignore
        self.windowSize = (0, 0)
        self.updateScreenResolution(window)
        self.listen(events.onWindowUpdate, self.updateScreenResolution)

    def updateScreenResolution(self, win: GraphicsWindow) -> None:
        newSize = (win.getXSize(), win.getYSize())
        if newSize[0] == self.windowSize[0] and newSize[1] == self.windowSize[1]:
            return

        self.windowSize = newSize
        self.base.render.setShaderInput("window_size", self.windowSize)
