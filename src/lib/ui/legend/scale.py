from __future__ import annotations

from typing import List

from panda3d.core import NodePath, PandaNode

from lib.app.state import AppState
from lib.model.data_type import DataType
from lib.ui.context import UIContext
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.colors import UIColors
from lib.ui.core.components.background_card import BackgroundCard
from lib.ui.core.components.component import Component
from lib.ui.core.components.image import Image
from lib.ui.core.components.text import Text
from lib.ui.core.constants import UIConstants
from lib.ui.core.layers import UILayer
from lib.util.events.listener import Listener


class Scale(Listener):
    def __init__(self, ctx: UIContext, state: AppState):
        super().__init__()

        self.ctx = ctx

        self.background = BackgroundCard(
            ctx.anchors.right,
            width=UIConstants.legendScaleWidth,
            height=UIConstants.legendScaleHeight,
            x=-UIConstants.legendPadding,
            hAlign=HAlign.RIGHT,
            vAlign=VAlign.CENTER,
            color=UIColors.LEGEND_BACKGROUND,
        )

        self.components: List[Component] = []

        self.refRoot = self.createScale(
            ctx.anchors.right, dataType=DataType.REFLECTIVITY
        )
        self.velRoot = self.createScale(ctx.anchors.right, DataType.VELOCITY)

        self.updateDataType(state.dataType.value)
        self.listen(state.dataType, self.updateDataType)

    def createScale(
        self,
        root: NodePath[PandaNode],
        dataType: DataType,
    ) -> NodePath[PandaNode]:
        node = root.attachNewNode("scaleNode")
        node.setX(-UIConstants.legendPadding)

        title: str
        scale: str
        increments: List[int]

        if dataType == DataType.REFLECTIVITY:
            title = "dBZ"
            scale = "assets/reflectivity_scale.png"
            increments = [-20, -10, 0, 10, 20, 30, 40, 50, 60, 70, 80]
        if dataType == DataType.VELOCITY:
            title = "KT"
            scale = "assets/velocity_scale.png"
            increments = [-100, -80, -60, -40, -20, 0, 20, 40, 60, 80, 100]

        self.components.append(
            Text(
                root=node,
                font=self.ctx.fonts.mono,
                text=title,
                x=-(UIConstants.legendScaleWidth / 2),
                y=(UIConstants.legendScaleHeight / 2) - UIConstants.legendPadding,
                hAlign=HAlign.CENTER,
                vAlign=VAlign.TOP,
            )
        )

        self.components.append(
            Image(
                root=node,
                image=scale,
                width=UIConstants.legendScaleBarWidth,
                height=UIConstants.legendScaleBarHeight,
                x=-UIConstants.legendPadding,
                y=-UIConstants.legendScaleHeight / 2 + UIConstants.legendPadding * 2,
                hAlign=HAlign.RIGHT,
                vAlign=VAlign.BOTTOM,
                layer=UILayer.CONTENT,
                color=None,
            )
        )

        spacing = UIConstants.legendScaleBarHeight / (len(increments) - 1)

        for i, value in enumerate(increments):
            self.components.append(
                Text(
                    root=node,
                    font=self.ctx.fonts.mono,
                    text=str(value),
                    x=-(
                        UIConstants.legendPadding * 2 + UIConstants.legendScaleBarWidth
                    ),
                    y=-UIConstants.legendScaleHeight / 2
                    + UIConstants.legendPadding * 2
                    + i * spacing,
                    hAlign=HAlign.RIGHT,
                    vAlign=VAlign.CENTER,
                )
            )

        return node

    def updateDataType(self, dataType: DataType) -> None:
        self.refRoot.hide()
        self.velRoot.hide()

        if dataType == DataType.REFLECTIVITY:
            self.refRoot.show()
        if dataType == DataType.VELOCITY:
            self.velRoot.show()

    def destroy(self) -> None:
        super().destroy()

        self.background.destroy()
        for component in self.components:
            component.destroy()

        self.refRoot.removeNode()
        self.velRoot.removeNode()
