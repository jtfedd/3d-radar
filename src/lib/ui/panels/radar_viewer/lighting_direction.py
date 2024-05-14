from __future__ import annotations

from panda3d.core import NodePath, PandaNode

from lib.app.state import AppState
from lib.ui.context import UIContext
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.components.text import Text
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

        headingPickerX = UIConstants.panelPadding + (UIConstants.panelContentWidth / 4)
        self.headingPickerText = Text(
            self.root,
            ctx.fonts.bold,
            "Direction",
            x=headingPickerX,
            y=-UIConstants.panelHeaderHeight / 2,
            hAlign=HAlign.CENTER,
            vAlign=VAlign.CENTER,
        )

        self.headingPickerRoot = self.root.attachNewNode("heading-picker")
        self.headingPickerRoot.setX(headingPickerX)
        self.headingPickerRoot.setZ(
            -(UIConstants.panelHeaderHeight + (UIConstants.lightingParametersSize / 2))
        )
        self.headingPicker = AnglePicker(
            self.headingPickerRoot, ctx, state.directionalLightHeading, 360, 0
        )

        pitchPickerX = (
            UIConstants.panelWidth
            - UIConstants.panelPadding
            - (UIConstants.panelContentWidth / 4)
        )
        self.pitchPickerText = Text(
            self.root,
            ctx.fonts.bold,
            "Overhead Angle",
            x=pitchPickerX,
            y=-UIConstants.panelHeaderHeight / 2,
            hAlign=HAlign.CENTER,
            vAlign=VAlign.CENTER,
        )

        self.pitchPickerRoot = self.root.attachNewNode("pitch-picker")
        self.pitchPickerRoot.setX(pitchPickerX)
        self.pitchPickerRoot.setZ(
            -(UIConstants.panelHeaderHeight + (UIConstants.lightingParametersSize / 2))
        )
        self.pitchPicker = AnglePicker(
            self.pitchPickerRoot,
            ctx,
            state.directionalLightPitch,
            scale=-90,
            offset=270,
            centerOffset=UIConstants.lightingParametersIconSize / 2,
            showLimits=True,
        )

    def getHeight(self) -> float:
        return UIConstants.panelHeaderHeight + UIConstants.lightingParametersSize

    def destroy(self) -> None:
        self.headingPickerText.destroy()
        self.headingPicker.destroy()
        self.headingPickerRoot.removeNode()

        self.pitchPickerText.destroy()
        self.pitchPicker.destroy()
        self.pitchPickerRoot.removeNode()
