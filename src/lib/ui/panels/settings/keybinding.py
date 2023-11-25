from __future__ import annotations

from panda3d.core import NodePath, PandaNode

from lib.ui.context import UIContext
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.components.text_input import TextInput
from lib.ui.core.constants import UIConstants
from lib.ui.panels.components.label import ComponentLabel
from lib.ui.panels.core.panel_component import PanelComponent
from lib.util.events.listener import Listener
from lib.util.events.observable import Observable


class KeybindingInput(PanelComponent):
    def __init__(
        self,
        root: NodePath[PandaNode],
        ctx: UIContext,
        label: str,
        keybinding: Observable[str],
    ):
        super().__init__(root)

        self.ctx = ctx
        self.keybinding = keybinding

        self.listener = Listener()

        self.label = ComponentLabel(self.root, ctx, label)

        self.input = TextInput(
            ctx=ctx,
            root=self.root,
            font=ctx.fonts.regular,
            x=UIConstants.panelContentWidth + UIConstants.panelPadding,
            y=-UIConstants.panelInputHeight / 2,
            hAlign=HAlign.RIGHT,
            vAlign=VAlign.CENTER,
            width=UIConstants.panelContentWidth / 4,
            size=UIConstants.fontSizeRegular,
            initialText=self.keybinding.value,
        )

        self.listener.listen(self.input.onChange, self.keybinding.setValue)
        self.listener.listen(self.keybinding, self.input.setText)

    def getHeight(self) -> float:
        return UIConstants.panelInputHeight

    def destroy(self) -> None:
        super().destroy()

        self.listener.destroy()

        self.label.destroy()
        self.input.destroy()
