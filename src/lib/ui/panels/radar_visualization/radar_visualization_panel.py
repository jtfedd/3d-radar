from lib.app.state import AppState
from lib.ui.core.context import UIContext
from lib.ui.events import UIEvents
from lib.ui.panels.components.slider import SliderComponent
from lib.ui.panels.components.title import TitleComponent
from lib.ui.panels.core.panel_content import PanelContent


class RadarVisualizationPanel(PanelContent):
    def __init__(self, ctx: UIContext, state: AppState, events: UIEvents) -> None:
        super().__init__(ctx, state, events)

        self.addComponent(TitleComponent(self.root, ctx, "Volume Parameters"))

        self.minSlider = self.addComponent(
            SliderComponent(
                self.root,
                ctx,
                state.volumeMin,
                label="Min",
                valueRange=(0, 1),
            )
        )

        self.maxSlider = self.addComponent(
            SliderComponent(
                self.root,
                ctx,
                state.volumeMax,
                label="Max",
                valueRange=(0, 1),
            )
        )

        self.falloffSlider = self.addComponent(
            SliderComponent(
                self.root,
                ctx,
                state.volumeFalloff,
                label="Falloff",
                valueRange=(0, 1),
            )
        )

    def headerText(self) -> str:
        return "Radar Visualization"

    def destroy(self) -> None:
        super().destroy()
