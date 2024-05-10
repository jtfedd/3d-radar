from __future__ import annotations

from typing import Dict

from panda3d.core import NodePath, PandaNode, Vec3

from lib.app.context import AppContext
from lib.app.state import AppState
from lib.util.events.listener import Listener
from lib.util.uuid import uuid


class LightingDataProvider(Listener):
    def __init__(self, ctx: AppContext, state: AppState):
        super().__init__()

        self.ctx = ctx
        self.state = state

        self.nodes: Dict[str, NodePath[PandaNode]] = {}

        self.listen(state.ambientLightIntensity, self.updateAmbientLightIntensity)
        self.listen(
            state.directionalLightIntensity, self.updateDirectionalLightIntensity
        )
        self.listen(
            state.directionalLightDirection, self.updateDirectionalLightDirection
        )
        self.listen(state.shadowStrength, self.updateShadowStrength)

    def addNode(self, node: NodePath[PandaNode]) -> str:
        nodeID = uuid()
        self.nodes[nodeID] = node

        node.setShaderInputs(
            ambient_intensity=self.state.ambientLightIntensity.value,
            directional_intensity=self.state.directionalLightIntensity.value,
            directional_orientation=self.state.directionalLightDirection.value,
            shadow_strength=self.state.shadowStrength.value,
        )

        return nodeID

    def removeNode(self, nodeID: str) -> None:
        del self.nodes[nodeID]

    def updateAmbientLightIntensity(self, value: float) -> None:
        for node in self.nodes.values():
            node.setShaderInput("ambient_intensity", value)

    def updateDirectionalLightIntensity(self, value: float) -> None:
        for node in self.nodes.values():
            node.setShaderInput("directional_intensity", value)

    def updateDirectionalLightDirection(self, value: Vec3) -> None:
        for node in self.nodes.values():
            node.setShaderInput("directional_orientation", value)

    def updateShadowStrength(self, value: float) -> None:
        for node in self.nodes.values():
            node.setShaderInput("shadow_strength", value)
