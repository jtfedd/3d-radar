from __future__ import annotations

from direct.gui.DirectEntry import DirectEntry
from panda3d.core import DynamicTextFont, NodePath, PandaNode

from lib.app.focus.focusable import Focusable
from lib.ui.context import UIContext
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.colors import UIColors
from lib.ui.core.constants import UIConstants
from lib.ui.core.layers import UILayer
from lib.ui.core.util import correctYForTextAlignment, horizontalAlignToTextNodeAlign
from lib.util.events.event_dispatcher import EventDispatcher


class TextInput(Focusable):
    def __init__(
        self,
        ctx: UIContext,
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
        super().__init__(ctx.appContext.focusManager)

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
            text_align=horizontalAlignToTextNodeAlign(hAlign),
            command=self.onCommit,
            focusInCommand=self.onFocus,
            focusInExtraArgs=[True],
            focusOutCommand=self.onFocus,
            focusOutExtraArgs=[False],
        )

        self.entry.setBin("fixed", layer.value)

        self.onChange = EventDispatcher[str]()

    def onCommit(self, value: str) -> None:
        self.onChange.send(value)

    def setText(self, value: str) -> None:
        self.entry.enterText(value)

    def destroy(self) -> None:
        super().destroy()

        self.entry.destroy()
        self.onChange.close()
