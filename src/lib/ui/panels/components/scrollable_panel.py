import direct.gui.DirectGuiGlobals as DGG
from direct.gui.DirectScrolledFrame import DirectScrolledFrame
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.DirectObject import DirectObject

from lib.ui.core.colors import UIColors
from lib.ui.core.config import UIConfig
from lib.ui.core.constants import UIConstants


class ScrollablePanel(DirectObject):
    def __init__(self, config: UIConfig) -> None:
        self.config = config

        self.frame = DirectScrolledFrame(
            parent=config.anchors.topLeft,
            pos=(0, 0, -UIConstants.headerFooterHeight),
            manageScrollBars=False,
            autoHideScrollBars=False,
            frameColor=(1, 0, 0, 1),  # TODO make transparent
            scrollBarWidth=UIConstants.scrollbarWidth,
            verticalScroll_borderWidth=(0, 0),
            verticalScroll_frameColor=UIColors.LIGHTGRAY,
            verticalScroll_thumb_frameColor=UIColors.WHITE,
        )

        self.frame.horizontalScroll.hide()
        self.frame.verticalScroll.incButton.hide()
        self.frame.verticalScroll.decButton.hide()

        self.updateFrame()

        for i in range(50):
            OnscreenText(
                parent=self.frame.getCanvas(),
                text=str(i),
                pos=(0.25, -i / 10.0),
                scale=0.07,
            )

        self.inBounds = False
        self.frame["state"] = DGG.NORMAL
        self.frame.bind(DGG.WITHIN, lambda w, _: self.updateInBounds(w), [True])
        self.frame.bind(DGG.WITHOUT, lambda w, _: self.updateInBounds(w), [False])

        self.accept("wheel_up-up", self.handleScroll, [-1])
        self.accept("wheel_down-up", self.handleScroll, [1])

        self.windowSub = self.config.anchors.onUpdate.listen(
            lambda _: self.updateFrame()
        )

    def updateInBounds(self, inBounds: bool) -> None:
        self.inBounds = inBounds

    def handleScroll(self, direction: int) -> None:
        if not self.inBounds or self.frame.verticalScroll.isHidden():
            return

        self.frame.verticalScroll.scrollStep(direction)

    def updateFrame(self) -> None:
        frameHeight = self.getPanelHeight()
        canvasHeight = self.getContentHeight()
        canvasHeight = max(canvasHeight, frameHeight)

        self.frame["frameSize"] = (0, UIConstants.panelWidth, -frameHeight, 0)
        self.frame["canvasSize"] = (0, UIConstants.panelWidth, -canvasHeight, 0)
        self.frame.verticalScroll["range"] = (0, 1)
        self.frame.verticalScroll["pageSize"] = frameHeight / canvasHeight

        if canvasHeight <= frameHeight:
            self.frame.verticalScroll.hide()
            return

        self.frame.verticalScroll.show()
        self.frame.verticalScroll.setPos(
            UIConstants.panelWidth - UIConstants.scrollbarPadding, 0, -frameHeight / 2
        )
        self.frame.verticalScroll.setScale(
            1, 1, (frameHeight / 2) - UIConstants.scrollbarPadding
        )

        scrollSteps = (canvasHeight - frameHeight) * UIConstants.scrollSensitivity
        scrollSize = 1 / scrollSteps
        self.frame.verticalScroll["scrollSize"] = scrollSize

    def getPanelHeight(self) -> float:
        # TODO this needs to account for the UI scale
        # AND the fact that the panel itself will be scaled
        windowHeight = self.config.anchors.height
        headerFooterHeight = UIConstants.headerFooterHeight * self.config.anchors.scale

        absolutePanelHeight = windowHeight - (headerFooterHeight * 2)

        return absolutePanelHeight / self.config.anchors.scale

    def getContentHeight(self) -> float:
        # TODO needs to retrieve the content height from the stack manager
        return 5.0

    def destroy(self) -> None:
        self.ignoreAll()
        self.windowSub.cancel()
        self.frame.destroy()
