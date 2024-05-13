from __future__ import annotations

from panda3d.core import NodePath, PandaNode

from lib.app.state import AppState
from lib.ui.context import UIContext
from lib.ui.core.constants import UIConstants
from lib.ui.panels.core.panel_component import PanelComponent

from .angle_picker import AnglePicker


class LightingDirection(PanelComponent):
    def __init__(
        self,
        root: NodePath[PandaNode],
        ctx: UIContext,
        state: AppState,
    ):
        super().__init__(root)

        self.headingPickerRoot = self.root.attachNewNode("heading-picker")
        self.headingPickerRoot.setX(
            UIConstants.panelPadding + (UIConstants.lightingParametersSize / 2)
        )
        self.headingPickerRoot.setZ(-UIConstants.lightingParametersSize / 2)
        self.headingPicker = AnglePicker(
            self.headingPickerRoot, ctx, state.directionalLightHeading, 360, 0
        )

        self.pitchPickerRoot = self.root.attachNewNode("pitch-picker")
        self.pitchPickerRoot.setX(
            UIConstants.panelWidth
            - UIConstants.panelPadding
            - (UIConstants.lightingParametersSize / 2)
        )
        self.pitchPickerRoot.setZ(-UIConstants.lightingParametersSize / 2)
        self.pitchPicker = AnglePicker(
            self.pitchPickerRoot,
            ctx,
            state.directionalLightPitch,
            -90,
            -90,
            centerOffset=UIConstants.lightingParametersIconSize / 2,
        )

    def getHeight(self) -> float:
        return UIConstants.lightingParametersSize

    def destroy(self) -> None:
        self.headingPicker.destroy()
        self.headingPickerRoot.removeNode()

        self.pitchPicker.destroy()
        self.pitchPickerRoot.removeNode()
