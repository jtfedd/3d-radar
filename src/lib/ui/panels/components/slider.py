from __future__ import annotations

from typing import Tuple

from panda3d.core import NodePath, PandaNode

from lib.ui.context import UIContext
from lib.ui.core.alignment import HAlign
from lib.ui.core.components.slider import Slider
from lib.ui.core.constants import UIConstants
from lib.ui.panels.components.label import ComponentLabel
from lib.ui.panels.core.panel_component import PanelComponent


class SliderComponent(PanelComponent):
    def __init__(
        self,
        root: NodePath[PandaNode],
        ctx: UIContext,
        initialValue: float,
        valueRange: Tuple[float, float],
        label: str,
        leftPadding: float = 0,
    ):
        super().__init__(root)

        self.ctx = ctx

        self.label = ComponentLabel(self.root, ctx, label)

        self.slider = Slider(
            root=self.root,
            x=UIConstants.panelPadding + UIConstants.panelContentWidth,
            y=-UIConstants.panelInputHeight / 2,
            width=UIConstants.panelSliderWidth - leftPadding,
            hAlign=HAlign.RIGHT,
            initialValue=initialValue,
            valueRange=valueRange,
        )

    def getHeight(self) -> float:
        return UIConstants.panelInputHeight

    def destroy(self) -> None:
        super().destroy()

        self.label.destroy()
        self.slider.destroy()
