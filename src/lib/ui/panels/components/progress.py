from __future__ import annotations

from panda3d.core import NodePath, PandaNode

from lib.app.context import AppContext
from lib.ui.core.alignment import HAlign
from lib.ui.core.components.progress_bar import ProgressBar
from lib.ui.core.constants import UIConstants
from lib.ui.panels.components.label import ComponentLabel
from lib.ui.panels.core.panel_component import PanelComponent


class ProgressComponent(PanelComponent):
    def __init__(
        self,
        root: NodePath[PandaNode],
        ctx: AppContext,
        progress: float,
        label: str,
        leftPadding: float = 0,
    ):
        super().__init__(root)

        self.ctx = ctx

        self.label = ComponentLabel(self.root, ctx, label)

        self.progressBar = ProgressBar(
            root=self.root,
            x=UIConstants.panelPadding + UIConstants.panelContentWidth,
            y=-UIConstants.panelInputHeight / 2,
            width=UIConstants.panelProgressWidth - leftPadding,
            hAlign=HAlign.RIGHT,
            progress=progress,
        )

    def getHeight(self) -> float:
        return UIConstants.panelInputHeight

    def destroy(self) -> None:
        super().destroy()

        self.label.destroy()
        self.progressBar.destroy()
