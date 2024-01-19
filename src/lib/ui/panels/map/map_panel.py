from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.ui.context import UIContext
from lib.ui.panels.components.button import PanelButton
from lib.ui.panels.components.checkbox import CheckboxComponent
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

        self.addComponent(TitleComponent(self.root, ctx, "Markers"))
        self.addMarkerButton = self.addComponent(
            PanelButton(self.root, ctx, "Add Marker")
        )

        self.listener.listen(
            self.addMarkerButton.button.onClick, events.ui.modals.markerAdd.send
        )

        self.addComponent(MarkersComponent(self.root, ctx, state, events))

    def headerText(self) -> str:
        return "Map"

    def destroy(self) -> None:
        super().destroy()

        self.listener.destroy()
