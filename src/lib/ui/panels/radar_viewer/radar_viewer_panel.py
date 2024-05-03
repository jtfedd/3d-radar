from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.ui.context import UIContext
from lib.ui.panels.components.checkbox import CheckboxComponent
from lib.ui.panels.components.slider import SliderComponent
from lib.ui.panels.components.title import TitleComponent
from lib.ui.panels.core.panel_content import PanelContent
from lib.util.events.listener import Listener


class RadarViewerPanel(PanelContent):
    def __init__(self, ctx: UIContext, state: AppState, events: AppEvents) -> None:
        super().__init__(ctx, state, events)

        self.state = state
        self.events = events
        self.listener = Listener()

        self.addComponent(TitleComponent(self.root, ctx, "Volume Parameters"))

        self.smoothCheckbox = self.addComponent(
            CheckboxComponent(self.root, ctx, "Smooth Shading", state.smooth)
        )

        self.minSlider = self.addComponent(
            SliderComponent(
                self.root,
                ctx,
                state.volumeMin.value,
                label="Min",
                valueRange=(0, 1),
            )
        )

        self.maxSlider = self.addComponent(
            SliderComponent(
                self.root,
                ctx,
                state.volumeMax.value,
                label="Max",
                valueRange=(0, 1),
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

        self.listener.listen(self.minSlider.slider.onValueChange, self.handleMinChange)
        self.listener.listen(self.maxSlider.slider.onValueChange, self.handleMaxChange)
        self.listener.listen(
            self.falloffSlider.slider.onValueChange, self.handleFalloffChange
        )

        self.listener.listen(self.state.volumeMin, self.minSlider.slider.setValue)
        self.listener.listen(self.state.volumeMax, self.maxSlider.slider.setValue)
        self.listener.listen(
            self.state.volumeFalloff, self.falloffSlider.slider.setValue
        )

    def handleMinChange(self, newMin: float) -> None:
        self.state.volumeMin.setValue(newMin)
        self.state.volumeMax.setValue(max(newMin, self.state.volumeMax.value))

    def handleMaxChange(self, newMax: float) -> None:
        self.state.volumeMax.setValue(newMax)
        self.state.volumeMin.setValue(min(newMax, self.state.volumeMin.value))

    def handleFalloffChange(self, newFalloff: float) -> None:
        self.state.volumeFalloff.setValue(newFalloff)

    def headerText(self) -> str:
        return "Radar Viewer"

    def destroy(self) -> None:
        super().destroy()
        self.listener.destroy()
