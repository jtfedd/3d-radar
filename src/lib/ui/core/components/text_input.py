from __future__ import annotations

from direct.gui.DirectEntry import DirectEntry
from panda3d.core import DynamicTextFont, NodePath, PandaNode, TextNode

from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.colors import UIColors
from lib.ui.core.config import UIConfig
from lib.ui.core.constants import UIConstants
from lib.ui.core.focus.focusable import Focusable
from lib.ui.core.layers import UILayer
from lib.ui.core.util import correctYForTextAlignment


class TextInput(Focusable):
    def __init__(
        self,
        config: UIConfig,
        root: NodePath[PandaNode],
        font: DynamicTextFont,
        size: float,
        width: float,
        x: float = 0,
        y: float = 0,
        hAlign: HAlign = HAlign.CENTER,
        vAlign: VAlign = VAlign.CENTER,
        layer: UILayer = UILayer.INTERACTION,
        initialText: str = "",
    ):
        super().__init__(config.focusManager)

        align = TextNode.ALeft
        if hAlign == HAlign.CENTER:
            align = TextNode.ACenter
        elif hAlign == HAlign.RIGHT:
            align = TextNode.ARight

        yPos = correctYForTextAlignment(y, font, size, vAlign)

        self.entry = DirectEntry(
            parent=root,
            text="",
            entryFont=font,
            initialText=initialText,
            pos=(x, 0, yPos),
            width=width / size,
            scale=size,
            borderWidth=(UIConstants.inputPadding, UIConstants.inputPadding),
            frameColor=UIColors.DARKGRAY,
            text_fg=UIColors.WHITE,
            text_align=align,
            command=self.onCommit,
            focusInCommand=self.onFocus,
            focusInExtraArgs=[True],
            focusOutCommand=self.onFocus,
            focusOutExtraArgs=[False],
        )

        self.entry.setBin("fixed", layer.value)

    def onCommit(self, value: str) -> None:
        print("commit " + value)
        self.entry.enterText("haha")

    def destroy(self) -> None:
        super().destroy()

        self.entry.destroy()
