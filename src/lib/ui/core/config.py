from typing import List

from direct.showbase.DirectObject import DirectObject
from direct.showbase.ShowBase import ShowBase
from panda3d.core import DynamicTextFont, GraphicsWindow

from lib.ui.core.anchors import UIAnchors
from lib.ui.core.constants import UIConstants
from lib.util.observable.observable import Observable


class UIConfig(DirectObject):
    def __init__(self, base: ShowBase, scale: float = 1.0) -> None:
        fontsize = 12

        self.font = DynamicTextFont("assets/font/Inter-Regular.ttf", 0)
        self.font.setPointSize(fontsize * 10)
        self.font.setPixelSize(fontsize)
        self.font.setSpaceAdvance(int(0.3 * fontsize))
        self.font.setLineHeight(int(1.2 * fontsize))
        self.font.setScaleFactor(1)

        window: GraphicsWindow = base.win  # type: ignore
        self.windowSize = (window.getXSize(), window.getYSize())
        self.accept("window-event", self.handleWindowEvent)

        self.anchors = UIAnchors(base.pixel2d, self.windowSize)

        self.scale = scale

        self.observables: List[Observable[float]] = []

        self.headerWidth = self.createObservable()
        self.headerHeight = self.createObservable()

        self.footerWidth = self.createObservable()
        self.footerHeight = self.createObservable()

        self.panelWidth = self.createObservable()

        self.update()

    def update(self) -> None:
        self.headerWidth.setValue(self.windowSize[0])
        self.headerHeight.setValue(UIConstants.headerFooterHeight * self.scale)

        self.footerWidth.setValue(self.windowSize[0])
        self.footerHeight.setValue(UIConstants.headerFooterHeight * self.scale)

        self.panelWidth.setValue(UIConstants.panelWidth * self.scale)

    def setScale(self, newScale: float) -> None:
        self.scale = newScale

        self.update()

    def handleWindowEvent(self, win: GraphicsWindow) -> None:
        newSize = (win.getXSize(), win.getYSize())
        if newSize[0] == self.windowSize[0] and newSize[1] == self.windowSize[1]:
            return

        self.windowSize = newSize

        self.anchors.update(newSize)

        self.update()

    def createObservable(self) -> Observable[float]:
        observable = Observable[float](0)
        self.observables.append(observable)
        return observable

    def destroy(self) -> None:
        for observable in self.observables:
            observable.close()

        self.ignoreAll()

        self.anchors.destroy()
