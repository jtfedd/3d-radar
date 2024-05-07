from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.ui.context import UIContext
from lib.ui.core.alignment import HAlign
from lib.ui.panels.components.button import PanelButton
from lib.ui.panels.components.button_group import PanelButtonGroup
from lib.ui.panels.components.checkbox import CheckboxComponent
from lib.ui.panels.components.slider import SliderComponent
from lib.ui.panels.components.spacer import SpacerComponent
from lib.ui.panels.components.text import PanelText
from lib.ui.panels.components.title import TitleComponent
from lib.ui.panels.core.panel_content import PanelContent
from lib.ui.panels.map.markers_component import MarkersComponent
from lib.util.events.listener import Listener


class MapPanel(PanelContent):
    def __init__(self, ctx: UIContext, state: AppState, events: AppEvents) -> None:
        super().__init__(ctx, state, events)

        self.listener = Listener()

        self.addComponent(TitleComponent(self.root, ctx, "Layers"))
        self.addComponent(CheckboxComponent(self.root, ctx, "States", state.mapStates))
        self.addComponent(
            CheckboxComponent(self.root, ctx, "Counties", state.mapCounties)
        )
        self.addComponent(CheckboxComponent(self.root, ctx, "Roads", state.mapRoads))

        self.addComponent(TitleComponent(self.root, ctx, "Warnings"))
        self.addComponent(
            PanelText(
                self.root,
                ctx,
                "Warnings are not shown when\nviewing historical data.",
                align=HAlign.CENTER,
                italic=True,
            )
        )
        self.addComponent(SpacerComponent(self.root))
        self.warningOpacitySlider = self.addComponent(
            SliderComponent(
                self.root,
                ctx,
                state.warningsOpacity.value,
                label="Opacity",
                valueRange=(0.3, 1),
            )
        )
        self.addComponent(
            CheckboxComponent(
                self.root, ctx, "Tornado Warnings", state.showTornadoWarnings
            )
        )
        self.addComponent(
            CheckboxComponent(
                self.root,
                ctx,
                "Severe Thunderstorm Warnings",
                state.showSevereThunderstormWarnings,
            )
        )

        self.addComponent(TitleComponent(self.root, ctx, "Markers"))

        self.addComponent(
            PanelButtonGroup(
                self.root,
                ctx,
                state.show3dMarkers,
                [("2D", False), ("3D", True)],
            )
        )

        self.addComponent(SpacerComponent(self.root))

        self.addMarkerButton = self.addComponent(
            PanelButton(self.root, ctx, "Add Marker")
        )

        self.listener.listen(
            self.addMarkerButton.button.onClick, events.ui.modals.markerAdd.send
        )

        self.addComponent(SpacerComponent(self.root))
        self.addComponent(MarkersComponent(self.root, ctx, state, events))
        self.addComponent(SpacerComponent(self.root))

        self.listener.listen(
            self.warningOpacitySlider.slider.onValueChange,
            state.warningsOpacity.setValue,
        )
        self.listener.listen(
            state.warningsOpacity,
            self.warningOpacitySlider.slider.setValue,
        )

    def headerText(self) -> str:
        return "Map"

    def destroy(self) -> None:
        super().destroy()

        self.listener.destroy()
