from direct.gui.OnscreenImage import OnscreenImage
from direct.showbase.DirectObject import DirectObject
from direct.showbase.ShowBase import ShowBase
from panda3d.core import TransparencyAttrib

from lib.ui.core.config import UIConfig
from lib.ui.ui import UI


class App(DirectObject):
    def __init__(self, showbase: ShowBase) -> None:
        self.base = showbase

        self.uiConfig = UIConfig(base)
        self.ui = UI(self.uiConfig)

        base.graphicsEngine.renderFrame()
        base.graphicsEngine.renderFrame()
        base.graphicsEngine.renderFrame()
        base.graphicsEngine.renderFrame()
        base.graphicsEngine.renderFrame()

        page = self.uiConfig.font.getPage(0)

        image = OnscreenImage(
            image=page,
            pos=(
                page.getXSize() / 2,
                0,
                (-page.getYSize() / 2) - self.uiConfig.headerHeight.value,
            ),
            scale=(page.getXSize() / 2, 1, page.getYSize() / 2),
            parent=self.uiConfig.anchors.topLeft,
        )
        image.setTransparency(TransparencyAttrib.MAlpha)


base = ShowBase()

app = App(base)
base.run()
