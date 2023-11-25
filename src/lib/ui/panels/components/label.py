from __future__ import annotations

from panda3d.core import NodePath, PandaNode

from lib.ui.context import UIContext
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.components.text import Text
from lib.ui.core.constants import UIConstants


class ComponentLabel:
    def __init__(self, root: NodePath[PandaNode], ctx: UIContext, text: str):
        self.label = Text(
            root=root,
            font=ctx.fonts.bold,
            text=text,
            x=UIConstants.panelPadding,
            y=-UIConstants.panelInputHeight / 2,
            hAlign=HAlign.LEFT,
            vAlign=VAlign.CENTER,
        )

    def destroy(self) -> None:
        self.label.destroy()
