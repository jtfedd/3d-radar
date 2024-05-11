from __future__ import annotations

import math
from typing import Dict

from panda3d.core import GeomEnums, NodePath, PandaNode, PTA_float, PTA_int, Texture

from lib.app.context import AppContext
from lib.app.state import AppState
from lib.model.data_type import DataType
from lib.model.scan import Scan
from lib.util import util
from lib.util.events.listener import Listener
from lib.util.uuid import uuid


class VolumeDataProvider(Listener):
    MAX_SCANS = 20

    def __init__(self, ctx: AppContext, state: AppState) -> None:
        super().__init__()
        self.ctx = ctx
        self.state = state

        self.nodes: Dict[str, NodePath[PandaNode]] = {}

        self.reflectivityScale = ctx.base.loader.loadTexture(
            "assets/reflectivity_scale.png",
        )
        self.velocityScale = ctx.base.loader.loadTexture(
            "assets/velocity_scale.png",
        )

        self.scanCount = PTA_int.empty_array(1)
        self.elevations = PTA_float.emptyArray(self.MAX_SCANS)
        self.azSteps = PTA_float.emptyArray(self.MAX_SCANS)
        self.azCounts = PTA_float.emptyArray(self.MAX_SCANS)
        self.rFirsts = PTA_float.emptyArray(self.MAX_SCANS)
        self.rSteps = PTA_float.emptyArray(self.MAX_SCANS)
        self.rCounts = PTA_int.emptyArray(self.MAX_SCANS)
        self.offsets = PTA_int.emptyArray(self.MAX_SCANS)

        # 0 = offset
        # 1 = factor
        # 2 = min
        # 3 = scale
        # 4 = exp
        # 5 = low
        # 6 = high
        self.densityParams = PTA_float.emptyArray(7)

        self.bufferSize = 0
        self.buffer = Texture("volume_data")
        self.setupBuffer()

        self.updateDensityParams()
        self.listen(self.state.rMin, lambda _: self.updateDensityParams())
        self.listen(self.state.rMax, lambda _: self.updateDensityParams())
        self.listen(self.state.rFalloff, lambda _: self.updateDensityParams())
        self.listen(self.state.rLowCut, lambda _: self.updateDensityParams())
        self.listen(self.state.rHighCut, lambda _: self.updateDensityParams())
        self.listen(self.state.vMin, lambda _: self.updateDensityParams())
        self.listen(self.state.vMax, lambda _: self.updateDensityParams())
        self.listen(self.state.vFalloff, lambda _: self.updateDensityParams())
        self.listen(self.state.vLowCut, lambda _: self.updateDensityParams())
        self.listen(self.state.vHighCut, lambda _: self.updateDensityParams())

        self.bind(state.dataType, self.updateDataType)

        self.listen(state.animationFrame, lambda _: self.updateFrame())
        self.listen(state.dataType, lambda _: self.updateFrame())

    def addNode(self, node: NodePath[PandaNode]) -> str:
        nodeID = uuid()
        self.nodes[nodeID] = node

        node.setShaderInputs(
            scan_count=self.scanCount,
            elevation=self.elevations,
            az_step=self.azSteps,
            az_count=self.azCounts,
            r_first=self.rFirsts,
            r_step=self.rSteps,
            r_count=self.rCounts,
            offset=self.offsets,
            volume_data=self.buffer,
            density_params=self.densityParams,
            color_scale=self.currentScale(),
        )

        return nodeID

    def removeNode(self, nodeID: str) -> None:
        del self.nodes[nodeID]

    def setupBuffer(self) -> None:
        self.buffer.setupBufferTexture(
            int(self.bufferSize / 4),  # buffer size is in bytes
            Texture.T_float,
            Texture.F_r32,
            GeomEnums.UH_dynamic,
        )

    def currentScale(self) -> Texture:
        if self.state.dataType.value == DataType.REFLECTIVITY:
            return self.reflectivityScale
        return self.velocityScale

    def updateDataType(self, dataType: DataType) -> None:
        for node in self.nodes.values():
            node.setShaderInput("color_scale", self.currentScale())

        if dataType == DataType.REFLECTIVITY:
            self.densityParams[0] = 0
            self.densityParams[1] = 1
        else:
            self.densityParams[0] = -0.5
            self.densityParams[1] = 2

        self.updateDensityParams()

    def updateDensityParams(self) -> None:
        isRef = self.state.dataType.value == DataType.REFLECTIVITY

        # Params for rendering the volume
        densityMin = self.state.rMin.value if isRef else self.state.vMin.value
        densityMax = self.state.rMax.value if isRef else self.state.vMax.value
        densityScale = densityMax - densityMin

        falloff = self.state.rFalloff.value if isRef else self.state.vFalloff.value
        densityExp = math.pow(10, falloff)

        self.densityParams[2] = densityMin
        self.densityParams[3] = densityScale
        self.densityParams[4] = densityExp
        self.densityParams[5] = (
            self.state.rLowCut.value if isRef else self.state.vLowCut.value
        )
        self.densityParams[6] = (
            self.state.rHighCut.value if isRef else self.state.vHighCut.value
        )

    def updateVolumeData(self, scan: Scan) -> None:
        scanData = scan.reflectivity
        if self.state.dataType.value == DataType.VELOCITY:
            scanData = scan.velocity

        # Create a new buffer if necessary
        if self.bufferSize < len(scanData.data):
            self.bufferSize = util.nextPowerOf2(len(scanData.data))
            self.setupBuffer()

        # I would love to create a single memory view when the buffer is created
        # and reuse that. It also seems to be faster. But for some reason the data
        # is not sent properly that way.
        dataView = memoryview(self.buffer.modifyRamImage())  # type: ignore
        dataView[: len(scanData.data)] = scanData.data

        # At some point I would like to optimize all of these meta inputs into a packed
        # struct or something but it doesn't seem to be a performance issue yet

        self.scanCount.setElement(0, len(scanData.metas))

        for i, meta in enumerate(scanData.metas):
            self.elevations.setElement(i, meta.elevation)
            self.azSteps.setElement(i, meta.azStep)
            self.azCounts.setElement(i, meta.azCount)
            self.rFirsts.setElement(i, meta.rngFirst)
            self.rSteps.setElement(i, meta.rngStep)
            self.rCounts.setElement(i, meta.rngCount)
            self.offsets.setElement(i, meta.offset)

    def updateFrame(self) -> None:
        if not self.state.animationFrame.value:
            return

        scan = self.ctx.radarCache.get(self.state.animationFrame.value)
        if not scan:
            return

        self.updateVolumeData(scan)
