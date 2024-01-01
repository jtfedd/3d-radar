from __future__ import annotations

import direct.gui.DirectGuiGlobals as DGG
from direct.gui.DirectEntry import DirectEntry
from panda3d.core import DynamicTextFont, NodePath, PandaNode

from lib.app.events import AppEvents
from lib.app.focus.focusable import Focusable
from lib.ui.context import UIContext
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.colors import UIColors
from lib.ui.core.components.background_card import BackgroundCard
from lib.ui.core.constants import UIConstants
from lib.ui.core.layers import UILayer
from lib.ui.core.util import (
    correctYForTextAlignment,
    getBaseline,
    horizontalAlignToTextNodeAlign,
)
from lib.util.events.event_dispatcher import EventDispatcher
from lib.util.events.listener import Listener

from .component import Component


class TextInput(Focusable, Component):
    def __init__(
        self,
        ctx: UIContext,
        events: AppEvents,
        root: NodePath[PandaNode],
        font: DynamicTextFont,
        size: float,
        width: float,
        x: float = 0,
        y: float = 0,
        hAlign: HAlign = HAlign.CENTER,
        vAlign: VAlign = VAlign.CENTER,
        layer: UILayer = UILayer.CONTENT_INTERACTION,
        initialText: str = "",
        valid: bool = True,
    ):
        super().__init__(ctx.appContext.focusManager, events.input)
        self.listener = Listener()

        self.valid = valid

        yPos = correctYForTextAlignment(y, font, size, vAlign)

        self.entry = DirectEntry(
            parent=root,
            text="",
            entryFont=font,
            initialText=initialText,
            pos=(x, 0, yPos),
            width=width / size,
            scale=size,
            borderWidth=(
                UIConstants.inputPaddingVertical,
                UIConstants.inputPaddingHorizontal,
            ),
            frameColor=UIColors.INSET,
            text_fg=UIColors.CONTENT,
            text_align=horizontalAlignToTextNodeAlign(hAlign),
            focusInCommand=self.onFocus,
            focusInExtraArgs=[True],
            focusOutCommand=self.onFocus,
            focusOutExtraArgs=[False],
        )

        self.validationUnderline = BackgroundCard(
            root=root,
            width=width + (UIConstants.inputPaddingVertical) * size * 2,
            height=UIConstants.inputUnderlineHeight,
            x=x + UIConstants.inputPaddingVertical * size,
            y=yPos
            - getBaseline(font, size)
            - (UIConstants.inputPaddingHorizontal * size),
            color=UIColors.RED,
            hAlign=hAlign,
            vAlign=VAlign.TOP,
            layer=layer,
        )

        self.setValid(valid)

        self.entry.setBin("fixed", layer.value)

        self.onChange = EventDispatcher[str]()
        self.onCommit = EventDispatcher[str]()

        self.inBounds = False
        self.entry["state"] = DGG.NORMAL
        self.entry.bind(DGG.WITHIN, lambda w, _: self.updateInBounds(w), [True])
        self.entry.bind(DGG.WITHOUT, lambda w, _: self.updateInBounds(w), [False])

        self.entry.bind(DGG.TYPE, lambda _: self.onChange.send(self.entry.get()))
        self.entry.bind(DGG.ERASE, lambda _: self.onChange.send(self.entry.get()))

        self.listener.listen(events.input.leftMouse, lambda _: self.checkFocus())
        self.listener.listen(events.input.rightMouse, lambda _: self.checkFocus())

    def setValid(self, valid: bool) -> None:
        self.valid = valid

        if valid:
            self.validationUnderline.hide()
        else:
            self.validationUnderline.show()

    def focus(self) -> None:
        self.entry["focus"] = True

    def blur(self) -> None:
        self.entry["focus"] = False

    def onFocus(self, focused: bool) -> None:
        super().onFocus(focused)

        if not focused:
            self.onCommit.send(self.entry.get())

    def checkFocus(self) -> None:
        if self.inBounds:
            self.focus()
        else:
            self.blur()

    def updateInBounds(self, inBounds: bool) -> None:
        self.inBounds = inBounds

    def setText(self, value: str) -> None:
        self.entry.enterText(value)
        self.onChange.send(value)

    def destroy(self) -> None:
        super().destroy()
        self.listener.destroy()

        self.entry.destroy()
        self.onChange.close()
