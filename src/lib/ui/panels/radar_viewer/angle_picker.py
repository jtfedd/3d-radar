from __future__ import annotations

from panda3d.core import NodePath, PandaNode

from lib.ui.context import UIContext
from lib.ui.core.alignment import VAlign
from lib.ui.core.colors import UIColors
from lib.ui.core.components.button import Button, ButtonSkin
from lib.ui.core.components.image import Image
from lib.ui.core.constants import UIConstants
from lib.ui.core.icons import Icons
from lib.ui.core.layers import UILayer
from lib.util.events.listener import Listener
from lib.util.events.observable import Observable


class AnglePicker(Listener):
    def __init__(
        self,
        root: NodePath[PandaNode],
        ctx: UIContext,
        observable: Observable[float],
        scale: float,
        offset: float,
        centerOffset: float = 0,
    ):
        super().__init__()

        self.button = Button(
            root,
            ctx,
            width=UIConstants.lightingParametersSize,
            height=UIConstants.lightingParametersSize,
            skin=ButtonSkin.ACCENT,
        )

        self.sun = Image(
            root,
            image=Icons.SUN,
            x=centerOffset,
            y=centerOffset,
            width=UIConstants.lightingParametersIconSize,
            height=UIConstants.lightingParametersIconSize,
            color=UIColors.CONTENT,
            layer=UILayer.CONTENT,
        )

        self.arrowRoot = root.attachNewNode("arrow-root")
        self.arrowRoot.setX(centerOffset)
        self.arrowRoot.setZ(centerOffset)

        self.arrow = Image(
            self.arrowRoot,
            image=Icons.ARROW,
            width=UIConstants.lightingParametersIconSize,
            height=UIConstants.lightingParametersIconSize,
            x=0,
            y=UIConstants.lightingParametersIconSize / 2,
            vAlign=VAlign.BOTTOM,
            color=UIColors.CONTENT,
            layer=UILayer.CONTENT,
        )

        self.bind(
            observable,
            lambda value: self.arrowRoot.setR((scale * value) + offset),
        )

    def destroy(self) -> None:
        super().destroy()

        self.button.destroy()
        self.sun.destroy()
        self.arrow.destroy()

        self.arrowRoot.removeNode()
