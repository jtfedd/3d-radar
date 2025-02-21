from lib.app.context import AppContext
from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.model.data_type import DataType
from lib.ui.core.constants import UIConstants
from lib.ui.panels.components.button_group import PanelButtonGroup
from lib.ui.panels.components.checkbox import CheckboxComponent
from lib.ui.panels.components.slider import SliderComponent
from lib.ui.panels.components.spacer import SpacerComponent
from lib.ui.panels.components.title import TitleComponent
from lib.ui.panels.core.panel_content import PanelContent
from lib.util.events.listener import Listener
from lib.util.events.observable import Observable

from .density_graph import DensityGraph
from .lighting_direction import LightingDirection


class RadarViewerPanel(PanelContent):
    def __init__(self, ctx: AppContext, state: AppState, events: AppEvents) -> None:
        super().__init__(ctx, state, events)

        self.ctx = ctx
        self.state = state

        self.listener = Listener()

        self.addComponent(SpacerComponent(self.root))

        self.addComponent(
            PanelButtonGroup(
                self.root,
                ctx,
                state.dataType,
                [
                    ("Reflectivity", DataType.REFLECTIVITY),
                    ("Velocity", DataType.VELOCITY),
                ],
                height=UIConstants.panelInputHeight,
            )
        )

        self.addComponent(SpacerComponent(self.root))

        self.addComponent(TitleComponent(self.root, ctx, "Rendering Mode"))

        self.smoothCheckbox = self.addComponent(
            CheckboxComponent(self.root, ctx, "Smooth Shading", state.smooth)
        )

        self.volumetricLighting = self.addComponent(
            CheckboxComponent(
                self.root,
                ctx,
                "Volumetric Lighting",
                state.volumetricLighting,
            )
        )

        self.addComponent(TitleComponent(self.root, ctx, "Surface Layer"))

        self.addComponent(
            CheckboxComponent(
                self.root,
                ctx,
                "Show Surface Layer",
                state.showSurfaceLayer,
            )
        )

        self.addComponent(SpacerComponent(self.root))

        self.surfaceOpacitySlider = self.addComponent(
            SliderComponent(
                self.root,
                ctx,
                self.state.surfaceOpacity.getValue(),
                (0.0, 1.0),
                "Opacity:",
            )
        )
        self.listener.listen(
            self.surfaceOpacitySlider.slider.onValueChange,
            self.state.surfaceOpacity.setValue,
        )

        self.createSurfaceControls(
            self.state.refThreshold,
            self.state.refComposite,
            DataType.REFLECTIVITY,
        )

        self.createSurfaceControls(
            self.state.velThreshold,
            self.state.velComposite,
            DataType.VELOCITY,
        )

        self.addComponent(TitleComponent(self.root, ctx, "Volume Parameters"))

        self.createVolumeControls(
            state.rLowCut,
            state.rHighCut,
            state.rMin,
            state.rMax,
            state.rFalloff,
            DataType.REFLECTIVITY,
        )

        self.createVolumeControls(
            state.vLowCut,
            state.vHighCut,
            state.vMin,
            state.vMax,
            state.vFalloff,
            DataType.VELOCITY,
        )

        self.addComponent(TitleComponent(self.root, ctx, "Ambient Lighting"))

        self.ambientIntensitySlider = self.addComponent(
            SliderComponent(
                self.root,
                ctx,
                state.ambientLightIntensity.value,
                label="Intensity",
                valueRange=(0, 1),
            )
        )
        self.linkSlider(state.ambientLightIntensity, self.ambientIntensitySlider)

        self.addComponent(TitleComponent(self.root, ctx, "Directional Lighting"))

        self.directionalIntensitySlider = self.addComponent(
            SliderComponent(
                self.root,
                ctx,
                state.directionalLightIntensity.value,
                label="Intensity",
                valueRange=(0, 1),
            )
        )
        self.linkSlider(
            state.directionalLightIntensity, self.directionalIntensitySlider
        )

        self.lightingDirection = self.addComponent(
            LightingDirection(self.root, ctx, state)
        )

    def createSurfaceControls(
        self,
        threshold: Observable[float],
        composite: Observable[bool],
        dataType: DataType,
    ) -> None:
        thresholdSlider = self.addComponent(
            SliderComponent(
                self.root,
                self.ctx,
                threshold.getValue(),
                (0.0, 1.0),
                "Threshold:",
            )
        )
        self.listener.listen(
            thresholdSlider.slider.onValueChange,
            threshold.setValue,
        )

        spacer = self.addComponent(SpacerComponent(self.root))

        compositeButtonGroup = self.addComponent(
            PanelButtonGroup(
                self.root,
                self.ctx,
                composite,
                [
                    ("Base", False),
                    ("Composite", True),
                ],
                label="Mode:",
                left=UIConstants.panelContentWidth - UIConstants.panelSliderWidth,
            )
        )

        self.listener.bind(
            self.state.dataType,
            lambda dt: thresholdSlider.setHidden(dt != dataType),
        )
        self.listener.bind(
            self.state.dataType,
            lambda dt: spacer.setHidden(dt != dataType),
        )
        self.listener.bind(
            self.state.dataType,
            lambda dt: compositeButtonGroup.setHidden(dt != dataType),
        )

    def createVolumeControls(
        self,
        low: Observable[float],
        high: Observable[float],
        minVal: Observable[float],
        maxVal: Observable[float],
        falloff: Observable[float],
        dataType: DataType,
    ) -> None:
        graph = self.addComponent(
            DensityGraph(self.root, low, high, minVal, maxVal, falloff, dataType)
        )

        lowCutSlider = self.addComponent(
            SliderComponent(
                self.root,
                self.ctx,
                low.value,
                label="Low Cut",
                valueRange=(0, 1),
            )
        )

        highCutSlider = self.addComponent(
            SliderComponent(
                self.root,
                self.ctx,
                high.value,
                label="High Cut",
                valueRange=(0, 1),
            )
        )

        minSlider = self.addComponent(
            SliderComponent(
                self.root,
                self.ctx,
                minVal.value,
                label="Min",
                valueRange=(0, 0.1),
            )
        )

        maxSlider = self.addComponent(
            SliderComponent(
                self.root,
                self.ctx,
                maxVal.value,
                label="Max",
                valueRange=(0, 10),
            )
        )

        falloffSlider = self.addComponent(
            SliderComponent(
                self.root,
                self.ctx,
                falloff.value,
                label="Falloff",
                valueRange=(0, 1),
            )
        )

        self.linkSlider(low, lowCutSlider)
        self.linkSlider(high, highCutSlider)
        self.linkSlider(minVal, minSlider)
        self.linkSlider(maxVal, maxSlider)
        self.linkSlider(falloff, falloffSlider)

        self.listener.listen(
            minSlider.slider.onValueChange,
            lambda value: maxVal.setValue(max(value, maxVal.value)),
        )

        self.listener.listen(
            maxSlider.slider.onValueChange,
            lambda value: minVal.setValue(min(value, minVal.value)),
        )

        self.listener.listen(
            lowCutSlider.slider.onValueChange,
            lambda value: high.setValue(max(value, high.value)),
        )

        self.listener.listen(
            highCutSlider.slider.onValueChange,
            lambda value: low.setValue(min(value, low.value)),
        )

        self.listener.bind(
            self.state.dataType, lambda dt: graph.setHidden(dt != dataType)
        )
        self.listener.bind(
            self.state.dataType, lambda dt: lowCutSlider.setHidden(dt != dataType)
        )
        self.listener.bind(
            self.state.dataType, lambda dt: highCutSlider.setHidden(dt != dataType)
        )
        self.listener.bind(
            self.state.dataType, lambda dt: minSlider.setHidden(dt != dataType)
        )
        self.listener.bind(
            self.state.dataType, lambda dt: maxSlider.setHidden(dt != dataType)
        )
        self.listener.bind(
            self.state.dataType, lambda dt: falloffSlider.setHidden(dt != dataType)
        )

    def linkSlider(
        self, observable: Observable[float], slider: SliderComponent
    ) -> None:
        self.listener.listen(slider.slider.onValueChange, observable.setValue)
        self.listener.listen(observable, slider.slider.setValue)

    def headerText(self) -> str:
        return "Radar Viewer"

    def destroy(self) -> None:
        super().destroy()
        self.listener.destroy()
