from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.model.data_type import DataType
from lib.ui.context import UIContext
from lib.ui.panels.components.checkbox import CheckboxComponent
from lib.ui.panels.components.slider import SliderComponent
from lib.ui.panels.components.title import TitleComponent
from lib.ui.panels.core.panel_content import PanelContent
from lib.util.events.listener import Listener
from lib.util.events.observable import Observable


class RadarViewerPanel(PanelContent):
    def __init__(self, ctx: UIContext, state: AppState, events: AppEvents) -> None:
        super().__init__(ctx, state, events)

        self.ctx = ctx
        self.state = state

        self.listener = Listener()

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

        self.addComponent(TitleComponent(self.root, ctx, "Lighting"))

        self.ambientIntensitySlider = self.addComponent(
            SliderComponent(
                self.root,
                ctx,
                state.ambientLightIntensity.value,
                label="Ambient",
                valueRange=(0, 1),
            )
        )

        self.directionalIntensitySlider = self.addComponent(
            SliderComponent(
                self.root,
                ctx,
                state.directionalLightIntensity.value,
                label="Directional",
                valueRange=(0, 1),
            )
        )

        self.directionalHeading = self.addComponent(
            SliderComponent(
                self.root,
                ctx,
                state.directionalLightHeading.value,
                label="Heading",
                valueRange=(0, 1),
            )
        )

        self.directionalPitch = self.addComponent(
            SliderComponent(
                self.root,
                ctx,
                state.directionalLightPitch.value,
                label="Angle",
                valueRange=(0, 1),
            )
        )

        self.linkSlider(state.ambientLightIntensity, self.ambientIntensitySlider)
        self.linkSlider(
            state.directionalLightIntensity, self.directionalIntensitySlider
        )
        self.linkSlider(state.directionalLightHeading, self.directionalHeading)
        self.linkSlider(state.directionalLightPitch, self.directionalPitch)

    def createVolumeControls(
        self,
        low: Observable[float],
        high: Observable[float],
        minVal: Observable[float],
        maxVal: Observable[float],
        falloff: Observable[float],
        dataType: DataType,
    ) -> None:
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
