from __future__ import annotations

from panda3d.core import NodePath, PandaNode

from lib.app.events import AppEvents
from lib.ui.context import UIContext
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.colors import UIColors
from lib.ui.core.components.text import Text
from lib.ui.core.components.text_input import TextInput
from lib.ui.core.constants import UIConstants
from lib.ui.panels.components.label import ComponentLabel
from lib.ui.panels.core.panel_component import PanelComponent
from lib.util.events.event_dispatcher import EventDispatcher
from lib.util.events.listener import Listener


class PanelTextInput(PanelComponent):
    def __init__(
        self,
        root: NodePath[PandaNode],
        ctx: UIContext,
        events: AppEvents,
        label: str,
        initialValue: str,
        inputWidth: float,
        rightMargin: float = 0,
        valid: bool = True,
        validationText: str = "",
    ):
        super().__init__(root)

        self.ctx = ctx
        self.valid = valid
        self.validationText = validationText

        self.listener = Listener()

        self.label = ComponentLabel(self.root, ctx, label)

        self.input = TextInput(
            ctx=ctx,
            events=events,
            root=self.root,
            font=ctx.fonts.regular,
            x=UIConstants.panelContentWidth
            + UIConstants.panelPadding
            - rightMargin
            - (UIConstants.inputPaddingVertical * UIConstants.fontSizeRegular),
            y=-UIConstants.panelInputHeight / 2,
            hAlign=HAlign.RIGHT,
            vAlign=VAlign.CENTER,
            width=inputWidth,
            size=UIConstants.fontSizeRegular,
            initialText=initialValue,
            valid=valid,
        )

        self.validationAlert = Text(
            root=self.root,
            font=ctx.fonts.regular,
            text=validationText,
            x=UIConstants.panelPadding + UIConstants.panelContentWidth,
            y=-UIConstants.panelInputHeight,
            hAlign=HAlign.RIGHT,
            vAlign=VAlign.TOP,
            size=UIConstants.fontSizeDetail,
            color=UIColors.RED,
        )

        self.setValid(valid)

        self.onChange = EventDispatcher[str]()

        self.listener.listen(self.input.onCommit, self.onChange.send)

    def setValid(self, valid: bool) -> None:
        self.input.setValid(valid)

        self.valid = valid

        if valid:
            self.validationAlert.hide()
        else:
            self.validationAlert.show()

        self.onHeightChange.send(None)

    def getHeight(self) -> float:
        height = UIConstants.panelInputHeight

        if not self.valid and self.validationText != "":
            height += UIConstants.panelValidationHeight

        return height

    def destroy(self) -> None:
        super().destroy()

        self.listener.destroy()
        self.onChange.close()

        self.label.destroy()
        self.input.destroy()
