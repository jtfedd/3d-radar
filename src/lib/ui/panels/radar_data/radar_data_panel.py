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

        self.ctx = ctx
        self.events = events
        self.state = state

        self.addComponent(SpacerComponent(self.root))

        self.radarInput = self.addComponent(
            PanelTextInput(
                self.root,
                ctx,
                events,
                "Radar Station:",
                state.station.value,
                UIConstants.panelContentWidth / 4,
            )
        )

        self.addComponent(TitleComponent(self.root, ctx, "Date and Time"))

        self.yearInput = self.addComponent(
            PanelTextInput(
                self.root,
                ctx,
                events,
                "Year:",
                str(state.year.value),
                UIConstants.panelContentWidth / 4,
            )
        )

        self.monthInput = self.addComponent(
            PanelTextInput(
                self.root,
                ctx,
                events,
                "Month:",
                str(state.month.value),
                UIConstants.panelContentWidth / 4,
            )
        )

        self.dayInput = self.addComponent(
            PanelTextInput(
                self.root,
                ctx,
                events,
                "Day:",
                str(state.day.value),
                UIConstants.panelContentWidth / 4,
            )
        )

        self.timeInput = self.addComponent(
            PanelTextInput(
                self.root,
                ctx,
                events,
                "Time:",
                state.time.value,
                UIConstants.panelContentWidth / 4,
            )
        )

        self.addComponent(SpacerComponent(self.root))

        loadDataButton = self.addComponent(
            PanelButton(
                self.root,
                ctx,
                "Load Data",
            )
        )

        loadDataButton.button.onClick.listen(lambda _: self.search())

    def search(self) -> None:
        radar = self.radarInput.input.entry.get()
        year = int(self.yearInput.input.entry.get())
        month = int(self.monthInput.input.entry.get())
        day = int(self.dayInput.input.entry.get())
        time = self.timeInput.input.entry.get()

        self.state.station.setValue(radar)
        self.state.year.setValue(year)
        self.state.month.setValue(month)
        self.state.day.setValue(day)
        self.state.time.setValue(time)

        self.events.requestData.send(None)

    def headerText(self) -> str:
        return "Radar Data"
