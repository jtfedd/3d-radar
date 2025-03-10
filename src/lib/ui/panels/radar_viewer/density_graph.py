from __future__ import annotations

import math
from typing import Callable

from panda3d.core import NodePath, PandaNode, PNMBrush, PNMImage, PNMPainter, Texture

from lib.model.data_type import DataType
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.colors import UIColors
from lib.ui.core.components.image import Image
from lib.ui.core.constants import UIConstants
from lib.ui.core.layers import UILayer
from lib.ui.panels.core.panel_component import PanelComponent
from lib.util.events.listener import Listener
from lib.util.events.observable import Observable


class DensityGraph(PanelComponent):
    def __init__(
        self,
        root: NodePath[PandaNode],
        low: Observable[float],
        high: Observable[float],
        minVal: Observable[float],
        maxVal: Observable[float],
        falloff: Observable[float],
        dataType: DataType,
    ):
        super().__init__(root)
        self.listener = Listener()

        self.low = low
        self.high = high
        self.min = minVal
        self.max = maxVal
        self.falloff = falloff
        self.dataType = dataType

        self.graphImage = PNMImage(
            UIConstants.densityGraphWidthPx, UIConstants.densityGraphHeightPx
        )
        self.graphTexture = Texture()

        self.graph = Image(
            self.root,
            image=self.graphTexture,
            width=UIConstants.panelContentWidth,
            height=-UIConstants.densityGraphHeight,
            x=UIConstants.panelPadding,
            y=0,
            color=UIColors.WHITE,
            hAlign=HAlign.LEFT,
            vAlign=VAlign.BOTTOM,
            layer=UILayer.CONTENT,
        )

        self.legendRoot = self.root.attachNewNode("legend-root")
        self.legendRoot.setX(UIConstants.panelPadding)
        self.legendRoot.setZ(-UIConstants.densityGraphHeight)
        self.legendRoot.setR(90)

        self.legend = Image(
            self.legendRoot,
            image=(
                "assets/reflectivity_scale.png"
                if dataType == DataType.REFLECTIVITY
                else "assets/velocity_scale.png"
            ),
            width=UIConstants.densityLegendHeight,
            height=UIConstants.panelContentWidth,
            color=UIColors.WHITE,
            hAlign=HAlign.LEFT,
            vAlign=VAlign.BOTTOM,
            layer=UILayer.CONTENT,
        )

        self.listener.listen(self.min, lambda _: self.updateGraph())
        self.listener.listen(self.max, lambda _: self.updateGraph())
        self.listener.listen(self.low, lambda _: self.updateGraph())
        self.listener.listen(self.high, lambda _: self.updateGraph())
        self.listener.listen(self.falloff, lambda _: self.updateGraph())

        self.updateGraph()

    def updateGraph(self) -> None:
        self.drawGraph()
        self.graphTexture.load(self.graphImage)

    def drawGraph(self) -> None:
        self.graphImage.fill(UIColors.ACCENT.x, UIColors.ACCENT.y, UIColors.ACCENT.z)

        graphMax = max(1, math.ceil(self.max.value))
        scale = UIConstants.densityGraphContentHeight / graphMax

        painter = PNMPainter(self.graphImage)

        self.drawScaleLines(painter, graphMax, scale)
        self.drawHorizontalComponents(painter, self.drawCutoffLines, scale)
        self.drawHorizontalComponents(painter, self.drawCutoffMarkers, scale)
        self.drawHorizontalComponents(painter, self.drawMinMaxLines, scale)
        self.drawHorizontalComponents(painter, self.drawFalloffGraph, scale)

    def drawHorizontalComponents(
        self,
        painter: PNMPainter,
        draw: Callable[[PNMPainter, Callable[[float], float], float], None],
        scale: float,
    ) -> None:
        draw(painter, lambda value: value, scale)
        if self.dataType == DataType.VELOCITY:
            draw(painter, lambda value: -value, scale)

    def drawFalloffGraph(
        self,
        painter: PNMPainter,
        transform: Callable[[float], float],
        scale: float,
    ) -> None:
        painter.setPen(self.makeLinePen())

        if self.low.value == self.high.value:
            minY = UIConstants.densityGraphPadding + (self.min.value * scale)
            maxY = UIConstants.densityGraphPadding + (self.max.value * scale)
            lowX = UIConstants.densityGraphContentWidth * self.normalize(
                transform(self.low.value)
            )
            highX = UIConstants.densityGraphContentWidth * self.normalize(
                transform(self.low.value)
            )

            painter.drawLine(lowX, minY, highX, maxY)
            return

        stepSize = (
            self.high.value - self.low.value
        ) / UIConstants.densityGraphFalloffSteps

        lastX = UIConstants.densityGraphContentWidth * self.normalize(
            transform(self.low.value)
        )
        lastY = UIConstants.densityGraphPadding + (self.min.value * scale)

        for i in range(UIConstants.densityGraphFalloffSteps):
            stepValue = self.low.value + ((i + 1) * stepSize)
            stepX = UIConstants.densityGraphContentWidth * self.normalize(
                transform(stepValue)
            )

            stepDensity = self.density(stepValue)
            stepY = UIConstants.densityGraphPadding + (stepDensity * scale)

            painter.drawLine(lastX, lastY, stepX, stepY)

            lastX = stepX
            lastY = stepY

    def density(self, value: float) -> float:
        value = (value - self.low.value) / (self.high.value - self.low.value)
        return self.min.value + (
            self.max.value * math.pow(value, math.pow(10, self.falloff.value))
        )

    def drawMinMaxLines(
        self,
        painter: PNMPainter,
        transform: Callable[[float], float],
        scale: float,
    ) -> None:
        painter.setPen(self.makeLinePen())

        if self.low.value > 0:
            minY = UIConstants.densityGraphPadding + (self.min.value * scale)
            painter.drawLine(
                UIConstants.densityGraphContentWidth * self.normalize(transform(0)),
                minY,
                UIConstants.densityGraphContentWidth
                * self.normalize(transform(self.low.value)),
                minY,
            )

        if self.high.value < 1:
            maxY = UIConstants.densityGraphPadding + (self.max.value * scale)
            painter.drawLine(
                UIConstants.densityGraphContentWidth
                * self.normalize(transform(self.high.value)),
                maxY,
                UIConstants.densityGraphContentWidth * self.normalize(transform(1)),
                maxY,
            )

    def drawCutoffMarkers(
        self,
        painter: PNMPainter,
        transform: Callable[[float], float],
        scale: float,
    ) -> None:
        painter.setPen(self.makePointPen())

        painter.drawPoint(
            UIConstants.densityGraphContentWidth
            * self.normalize(transform(self.low.value)),
            UIConstants.densityGraphPadding + (self.min.value * scale),
        )

        painter.drawPoint(
            UIConstants.densityGraphContentWidth
            * self.normalize(transform(self.high.value)),
            UIConstants.densityGraphPadding + (self.max.value * scale),
        )

    def drawCutoffLines(
        self,
        painter: PNMPainter,
        transform: Callable[[float], float],
        _: float,
    ) -> None:
        painter.setPen(self.makeDashedPen())

        self.drawVLine(
            painter,
            UIConstants.densityGraphContentWidth
            * self.normalize(transform(self.low.value)),
        )
        self.drawVLine(
            painter,
            UIConstants.densityGraphContentWidth
            * self.normalize(transform(self.high.value)),
        )

    def drawScaleLines(
        self,
        painter: PNMPainter,
        graphMax: int,
        scale: float,
    ) -> None:
        painter.setPen(self.makeDashedPen())

        for i in range(graphMax + 1):
            self.drawHLine(painter, UIConstants.densityGraphPadding + i * scale)

    def drawHLine(self, painter: PNMPainter, y: float) -> None:
        dashCount = math.ceil(
            UIConstants.densityGraphWidthPx / (2 * UIConstants.densityGraphDashLength)
        )

        for i in range(dashCount):
            dashStart = i * (UIConstants.densityGraphDashLength * 2)
            dashEnd = dashStart + UIConstants.densityGraphDashLength

            painter.drawLine(dashStart, y, dashEnd, y)

    def drawVLine(self, painter: PNMPainter, x: float) -> None:
        dashCount = math.ceil(
            UIConstants.densityGraphHeightPx / (2 * UIConstants.densityGraphDashLength)
        )

        for i in range(dashCount):
            dashStart = i * (UIConstants.densityGraphDashLength * 2)
            dashEnd = dashStart + UIConstants.densityGraphDashLength

            painter.drawLine(x, dashStart, x, dashEnd)

    def makeDashedPen(self) -> PNMBrush:
        return PNMBrush.makeSpot(
            color=UIColors.ACCENT_HOVER,
            radius=UIConstants.densityGraphDashedLineRadius,
            fuzzy=False,
        )

    def makeLinePen(self) -> PNMBrush:
        return PNMBrush.makeSpot(
            color=UIColors.CONTENT,
            radius=UIConstants.densityGraphLineRadius,
            fuzzy=False,
        )

    def makePointPen(self) -> PNMBrush:
        return PNMBrush.makeSpot(
            color=UIColors.CONTENT,
            radius=UIConstants.densityGraphPointRadius,
            fuzzy=False,
        )

    def normalize(self, value: float) -> float:
        if self.dataType == DataType.VELOCITY:
            return 0.5 + (value / 2)
        return value

    def getHeight(self) -> float:
        return (
            UIConstants.densityGraphHeight
            + UIConstants.densityLegendHeight
            + UIConstants.panelPadding
        )

    def destroy(self) -> None:
        super().destroy()
        self.listener.destroy()

        self.graph.destroy()
        self.legend.destroy()

        self.legendRoot.removeNode()
