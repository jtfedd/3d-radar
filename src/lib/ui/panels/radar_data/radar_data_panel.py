import datetime

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
                validationText="Unknown radar station",
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
                validationText="Invalid Year",
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
                validationText="Invalid Month",
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
                validationText="Invalid Day",
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
                validationText="Invalid Time",
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

        self.setupFocusLoop(
            [
                self.radarInput.input,
                self.yearInput.input,
                self.monthInput.input,
                self.dayInput.input,
                self.timeInput.input,
            ]
        )

    def resetValidation(self) -> None:
        self.radarInput.setValid(True)
        self.yearInput.setValid(True)
        self.monthInput.setValid(True)
        self.dayInput.setValid(True)
        self.timeInput.setValid(True)

    def search(self) -> None:
        valid = True

        self.resetValidation()

        radar = self.radarInput.input.entry.get()
        # Validate radar station

        try:
            year = int(self.yearInput.input.entry.get())
            if year < 1991 or year > 9999:
                raise ValueError("Invalid year value")
        except ValueError:
            valid = False
            self.yearInput.setValid(False)

        try:
            month = int(self.monthInput.input.entry.get())
            if month < 1 or month > 12:
                raise ValueError("Invalid month value")
        except ValueError:
            valid = False
            self.monthInput.setValid(False)

        try:
            day = int(self.dayInput.input.entry.get())
            if day < 1 or day > 31:
                raise ValueError("Invalid day value")
        except ValueError:
            valid = False
            self.dayInput.setValid(False)

        time = self.timeInput.input.entry.get()
        try:
            self.validateTime(time)
        except ValueError:
            valid = False
            self.timeInput.setValid(False)

        if not valid:
            return

        try:
            datetime.datetime(year=year, month=month, day=day)
        except ValueError:
            valid = False
            self.dayInput.setValid(False)

        if not valid:
            return

        self.state.station.setValue(radar)
        self.state.year.setValue(year)
        self.state.month.setValue(month)
        self.state.day.setValue(day)
        self.state.time.setValue(time)

        self.events.requestData.send(None)

    def validateTime(self, time: str) -> None:
        parts = time.split(":")
        if len(parts) != 2:
            raise ValueError("Time should be in the format HH:MM")

        hour = parts[0]
        minute = parts[1]

        if len(minute) != 2:
            raise ValueError("Minute should be formatted as MM")

        hourInt = int(hour)
        minuteInt = int(minute)

        if minuteInt < 0 or minuteInt > 59:
            raise ValueError("Minute invalid")

        # This should take into account 12/24 hour time eventually
        if hourInt < 1 or hourInt > 24:
            raise ValueError("Hour invalid")

    def validateYear(self, year: str) -> bool:
        try:
            yearInt = int(year)
        except ValueError:
            return False

        return 1991 <= yearInt

    def headerText(self) -> str:
        return "Radar Data"
