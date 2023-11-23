from __future__ import annotations

from typing import Tuple

from panda3d.core import NodePath, PandaNode

from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.components.slider import Slider
from lib.ui.core.components.text import Text
from lib.ui.core.constants import UIConstants
from lib.ui.core.context import UIContext
from lib.ui.panels.core.panel_component import PanelComponent
from lib.util.events.observable import Observable


class SliderComponent(PanelComponent):
    def __init__(
        self,
        root: NodePath[PandaNode],
        ctx: UIContext,
        valueObservable: Observable[float],
        valueRange: Tuple[float, float],
        label: str,
    ):
        super().__init__(root)

        self.ctx = ctx
        self.valueObservable = valueObservable

        self.label = Text(
            root=self.root,
            font=ctx.fonts.bold,
            text=label,
            x=UIConstants.panelPadding,
            y=-UIConstants.panelInputHeight / 2,
            hAlign=HAlign.LEFT,
            vAlign=VAlign.CENTER,
        )

        self.slider = Slider(
            root=self.root,
            x=UIConstants.panelPadding + UIConstants.panelContentWidth,
            y=-UIConstants.panelInputHeight / 2,
            width=UIConstants.panelSliderWidth,
            hAlign=HAlign.RIGHT,
            initialValue=valueObservable.value,
            valueRange=valueRange,
        )

    def getHeight(self) -> float:
        return UIConstants.panelInputHeight

    def destroy(self) -> None:
        super().destroy()

        self.label.destroy()
        self.slider.destroy()
