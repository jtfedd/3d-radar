from __future__ import annotations

from panda3d.core import NodePath, PandaNode

from lib.app.events import AppEvents
from lib.ui.context import UIContext
from lib.ui.core.alignment import HAlign, VAlign
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
    ):
        super().__init__(root)

        self.ctx = ctx

        self.listener = Listener()

        self.label = ComponentLabel(self.root, ctx, label)

        self.input = TextInput(
            ctx=ctx,
            events=events,
            root=self.root,
            font=ctx.fonts.regular,
            x=UIConstants.panelContentWidth + UIConstants.panelPadding,
            y=-UIConstants.panelInputHeight / 2,
            hAlign=HAlign.RIGHT,
            vAlign=VAlign.CENTER,
            width=inputWidth,
            size=UIConstants.fontSizeRegular,
            initialText=initialValue,
        )

        self.onChange = EventDispatcher[str]()

        self.listener.listen(self.input.onChange, self.onChange.send)

    def getHeight(self) -> float:
        return UIConstants.panelInputHeight

    def destroy(self) -> None:
        super().destroy()

        self.listener.destroy()
        self.onChange.close()

        self.label.destroy()
        self.input.destroy()
