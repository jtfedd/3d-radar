from lib.app.events import AppEvents
from lib.app.state import AppState
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

        self.lowCutSlider = self.addComponent(
            SliderComponent(
                self.root,
                ctx,
                state.volumeLowCut.value,
                label="Low Cut",
                valueRange=(0, 1),
            )
        )

        self.highCutSlider = self.addComponent(
            SliderComponent(
                self.root,
                ctx,
                state.volumeHighCut.value,
                label="High Cut",
                valueRange=(0, 1),
            )
        )

        self.minSlider = self.addComponent(
            SliderComponent(
                self.root,
                ctx,
                state.volumeMin.value,
                label="Min",
                valueRange=(0, 0.1),
            )
        )

        self.maxSlider = self.addComponent(
            SliderComponent(
                self.root,
                ctx,
                state.volumeMax.value,
                label="Max",
                valueRange=(0, 10),
            )
        )

        self.falloffSlider = self.addComponent(
            SliderComponent(
                self.root,
                ctx,
                state.volumeFalloff.value,
                label="Falloff",
                valueRange=(0, 1),
            )
        )

        self.linkSlider(state.volumeLowCut, self.lowCutSlider)
        self.linkSlider(state.volumeHighCut, self.highCutSlider)
        self.linkSlider(state.volumeMin, self.minSlider)
        self.linkSlider(state.volumeMax, self.maxSlider)
        self.linkSlider(state.volumeFalloff, self.falloffSlider)

        self.listener.listen(
            self.minSlider.slider.onValueChange,
            lambda value: state.volumeMax.setValue(max(value, state.volumeMax.value)),
        )

        self.listener.listen(
            self.maxSlider.slider.onValueChange,
            lambda value: state.volumeMin.setValue(min(value, state.volumeMin.value)),
        )

        self.listener.listen(
            self.lowCutSlider.slider.onValueChange,
            lambda value: state.volumeHighCut.setValue(
                max(value, state.volumeHighCut.value)
            ),
        )

        self.listener.listen(
            self.highCutSlider.slider.onValueChange,
            lambda value: state.volumeLowCut.setValue(
                min(value, state.volumeLowCut.value)
            ),
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
