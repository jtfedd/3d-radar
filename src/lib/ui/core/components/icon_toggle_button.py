from __future__ import annotations

import direct.gui.DirectGuiGlobals as DGG
from direct.gui.DirectButton import DirectButton
from direct.showbase.DirectObject import DirectObject
from direct.task.Task import Task
from panda3d.core import NodePath, PandaNode, TransparencyAttrib, Vec4

from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.colors import UIColors
from lib.ui.core.components.background_card import BackgroundCard
from lib.ui.core.layers import UILayer
from lib.ui.core.util import correctXForAlignment, correctYForAlignment
from lib.util.events.event_dispatcher import EventDispatcher


class IconToggleButton(DirectObject):
    def __init__(
        self,
        root: NodePath[PandaNode],
        icon: str,
        width: float,
        height: float,
        x: float = 0,
        y: float = 0,
        hAlign: HAlign = HAlign.CENTER,
        vAlign: VAlign = VAlign.CENTER,
        layer: UILayer = UILayer.CONTENT,
        readyColor: Vec4 = UIColors.TRANSPARENT,
        hoverColor: Vec4 = UIColors.WHITE,
        clickColor: Vec4 = UIColors.BLACK,
        disabledColor: Vec4 = UIColors.GRAY,
    ) -> None:
        xPos = correctXForAlignment(x, width, hAlign)
        yPos = correctYForAlignment(y, height, vAlign)

        self.colorMap = {
            DGG.BUTTON_READY_STATE: readyColor,
            DGG.BUTTON_ROLLOVER_STATE: hoverColor,
            DGG.BUTTON_DEPRESSED_STATE: clickColor,
            DGG.BUTTON_INACTIVE_STATE: disabledColor,
        }

        self.button = DirectButton(
            parent=root,
            image=icon,
            command=self.handleClick,
            pos=(xPos, 0, yPos),
            scale=(width / 2, 1, height / 2),
            borderWidth=(0, 0),
            frameColor=(0, 0, 0, 0),
            rolloverSound=None,
            clickSound=None,
        )

        self.background = BackgroundCard(
            root=root,
            width=width,
            height=height,
            x=x,
            y=y,
            hAlign=hAlign,
            vAlign=vAlign,
            color=UIColors.GRAY,
            layer=UILayer(layer.value - 1),
        )

        self.button.setBin("fixed", layer.value)
        self.button.setTransparency(TransparencyAttrib.MAlpha)

        self.onClick = EventDispatcher[bool]()

        self.addTask(self.update, "button-update")

    def update(self, task: Task) -> int:
        buttonState = self.button.guiItem.getState()  # type: ignore

        self.background.updateColor(self.colorMap[buttonState])

        return task.cont

    def handleClick(self) -> None:
        self.onClick.send(True)

    def destroy(self) -> None:
        self.removeAllTasks()
        self.button.destroy()
        self.background.destroy()
        self.onClick.close()
