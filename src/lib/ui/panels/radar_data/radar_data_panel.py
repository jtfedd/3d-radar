from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.ui.context import UIContext
from lib.ui.core.constants import UIConstants
from lib.ui.panels.components.button import PanelButton
from lib.ui.panels.components.spacer import SpacerComponent
from lib.ui.panels.components.text_input import PanelTextInput
from lib.ui.panels.components.title import TitleComponent
from lib.ui.panels.core.panel_content import PanelContent


class RadarDataPanel(PanelContent):
    def __init__(self, ctx: UIContext, state: AppState, events: AppEvents) -> None:
        super().__init__(ctx, state, events)

        self.addComponent(SpacerComponent(self.root))

        self.addComponent(
            PanelTextInput(
                self.root,
                ctx,
                events,
                "Radar Station:",
                "KDMX",
                UIConstants.panelContentWidth / 4,
            )
        )

        self.addComponent(TitleComponent(self.root, ctx, "Date and Time"))

        self.addComponent(
            PanelTextInput(
                self.root,
                ctx,
                events,
                "Year:",
                "2023",
                UIConstants.panelContentWidth / 4,
            )
        )

        self.addComponent(
            PanelTextInput(
                self.root,
                ctx,
                events,
                "Month:",
                "11",
                UIConstants.panelContentWidth / 4,
            )
        )

        self.addComponent(
            PanelTextInput(
                self.root,
                ctx,
                events,
                "Day:",
                "27",
                UIConstants.panelContentWidth / 4,
            )
        )

        self.addComponent(
            PanelTextInput(
                self.root,
                ctx,
                events,
                "Time:",
                "11:24",
                UIConstants.panelContentWidth / 4,
            )
        )

        self.addComponent(SpacerComponent(self.root))

        self.addComponent(
            PanelButton(
                self.root,
                ctx,
                "Load Data",
            )
        )

    def headerText(self) -> str:
        return "Radar Data"
