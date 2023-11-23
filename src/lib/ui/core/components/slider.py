from __future__ import annotations

from typing import Tuple

from direct.gui import DirectGuiGlobals as DGG
from direct.gui.DirectSlider import DirectSlider
from panda3d.core import NodePath, PandaNode, TransparencyAttrib

from lib.ui.core.alignment import HAlign
from lib.ui.core.colors import UIColors
from lib.ui.core.constants import UIConstants
from lib.ui.core.layers import UILayer
from lib.ui.core.util import correctXForAlignment
from lib.util.events.event_dispatcher import EventDispatcher


class Slider:
    def __init__(
        self,
        root: NodePath[PandaNode],
        x: float,
        y: float,
        width: float,
        hAlign: HAlign,
        initialValue: float,
        valueRange: Tuple[float, float],
        layer: UILayer = UILayer.INTERACTION,
    ) -> None:
        xPos = correctXForAlignment(x, width, hAlign)

        self.slider = DirectSlider(
            parent=root,
            pos=(xPos, 0, y),
            frameSize=(
                -width / 2,
                width / 2,
                UIConstants.sliderHeight / 2,
                -UIConstants.sliderHeight / 2,
            ),
            frameColor=UIColors.WHITE,
            range=valueRange,
            value=initialValue,
            pageSize=valueRange[1] - valueRange[0],
            thumb_frameSize=(
                -UIConstants.sliderHandleWidth,
                UIConstants.sliderHandleWidth,
                UIConstants.sliderHandleHeight,
                -UIConstants.sliderHandleHeight,
            ),
            thumb_frameColor=UIColors.WHITE,
            thumb_relief=DGG.FLAT,
        )

        self.slider.setTransparency(TransparencyAttrib.MAlpha)
        self.slider.setBin("fixed", layer.value)

        self.onValueChange = EventDispatcher[float]()

    def handleValueChange(self) -> None:
        self.onValueChange.send(float(self.slider["value"]))

    def setValue(self, value: float) -> None:
        self.slider.setValue(value)

    def destroy(self) -> None:
        self.onValueChange.close()
        self.slider.destroy()
