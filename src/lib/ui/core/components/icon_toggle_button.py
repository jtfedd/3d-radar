from __future__ import annotations

import direct.gui.DirectGuiGlobals as DGG
from direct.gui.DirectButton import DirectButton
from direct.task.Task import Task
from panda3d.core import NodePath, PandaNode, TransparencyAttrib

from lib.ui.context import UIContext
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.colors import UIColors
from lib.ui.core.components.background_card import BackgroundCard
from lib.ui.core.components.image import Image
from lib.ui.core.layers import UILayer
from lib.ui.core.util import correctXForAlignment, correctYForAlignment
from lib.util.events.event_dispatcher import EventDispatcher


class IconToggleButton:
    def __init__(
        self,
        root: NodePath[PandaNode],
        ctx: UIContext,
        icon: str,
        width: float,
        height: float,
        iconWidth: float,
        iconHeight: float,
        x: float = 0,
        y: float = 0,
        hAlign: HAlign = HAlign.CENTER,
        vAlign: VAlign = VAlign.CENTER,
        layer: UILayer = UILayer.INTERACTION,
        toggleState: bool = False,
    ) -> None:
        self.toggleState = toggleState

        xPos = correctXForAlignment(x, width, hAlign)
        yPos = correctYForAlignment(y, height, vAlign)

        self.backgroundColorMap = {
            DGG.BUTTON_READY_STATE: UIColors.TRANSPARENT,
            DGG.BUTTON_ROLLOVER_STATE: UIColors.LIGHTGRAY,
            DGG.BUTTON_DEPRESSED_STATE: UIColors.BLACK,
            DGG.BUTTON_INACTIVE_STATE: UIColors.GRAY,
        }

        self.iconColorMap = {
            DGG.BUTTON_READY_STATE: UIColors.WHITE,
            DGG.BUTTON_ROLLOVER_STATE: UIColors.WHITE,
            DGG.BUTTON_DEPRESSED_STATE: UIColors.WHITE,
            DGG.BUTTON_INACTIVE_STATE: UIColors.GRAY,
        }

        self.background = BackgroundCard(
            root=root,
            width=width,
            height=height,
            x=x,
            y=y,
            hAlign=hAlign,
            vAlign=vAlign,
            color=UIColors.GRAY,
            layer=UILayer(layer.value - 2),
        )

        self.icon = Image(
            root=root,
            image=icon,
            width=iconWidth,
            height=iconHeight,
            x=xPos,
            y=yPos,
            hAlign=HAlign.CENTER,
            vAlign=VAlign.CENTER,
            layer=UILayer(layer.value - 1),
        )

        self.button = DirectButton(
            parent=root,
            image="assets/white.png",
            command=self.handleClick,
            pos=(xPos, 0, yPos),
            scale=(width / 2, 1, height / 2),
            borderWidth=(0, 0),
            frameColor=UIColors.TRANSPARENT,
            rolloverSound=None,
            clickSound=None,
        )

        self.button.setBin("fixed", layer.value)
        self.button.setTransparency(TransparencyAttrib.MAlpha)
        self.button.setAlphaScale(0)

        self.onClick = EventDispatcher[None]()

        self.updateTask = ctx.appContext.base.addTask(self.update, "button-update")

    def update(self, task: Task) -> int:
        buttonState = self.button.guiItem.getState()  # type: ignore

        # Toggled state should override ready and hover
        if self.toggleState and buttonState in (
            DGG.BUTTON_READY_STATE,
            DGG.BUTTON_ROLLOVER_STATE,
        ):
            self.background.updateColor(UIColors.WHITE)
            self.icon.updateColor(UIColors.GRAY)
        else:
            self.background.updateColor(self.backgroundColorMap[buttonState])
            self.icon.updateColor(self.iconColorMap[buttonState])

        return task.cont

    def handleClick(self) -> None:
        self.onClick.send(None)

    def setToggleState(self, toggleState: bool) -> None:
        self.toggleState = toggleState

    def destroy(self) -> None:
        self.updateTask.cancel()
        self.button.destroy()
        self.background.destroy()
        self.icon.destroy()
        self.onClick.close()
