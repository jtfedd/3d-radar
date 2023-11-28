import datetime

from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.model.record import Record
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

        self.addComponent(SpacerComponent(self.root))

        self.radarInput = self.addComponent(
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

        self.yearInput = self.addComponent(
            PanelTextInput(
                self.root,
                ctx,
                events,
                "Year:",
                "2023",
                UIConstants.panelContentWidth / 4,
            )
        )

        self.monthInput = self.addComponent(
            PanelTextInput(
                self.root,
                ctx,
                events,
                "Month:",
                "11",
                UIConstants.panelContentWidth / 4,
            )
        )

        self.dayInput = self.addComponent(
            PanelTextInput(
                self.root,
                ctx,
                events,
                "Day:",
                "27",
                UIConstants.panelContentWidth / 4,
            )
        )

        self.timeInput = self.addComponent(
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
        hour = int(time.split(":")[0])
        minute = int(time.split(":")[1])

        records = self.ctx.appContext.network.search(
            Record(
                radar,
                datetime.datetime(
                    year=year,
                    month=month,
                    day=day,
                    hour=hour,
                    minute=minute,
                    tzinfo=datetime.timezone.utc,
                ),
            ),
            1,
        )

        if len(records) == 0:
            raise ValueError("No Records Found")

        self.events.ui.panels.requestData.send(records[0])

    def headerText(self) -> str:
        return "Radar Data"
