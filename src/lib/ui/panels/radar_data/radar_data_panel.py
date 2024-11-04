import datetime
from typing import List

from lib.app.events import AppEvents
from lib.app.focus.focusable import Focusable
from lib.app.state import AppState
from lib.model.data_query import DataQuery
from lib.model.time_query import TimeQuery
from lib.ui.context import UIContext
from lib.ui.core.constants import UIConstants
from lib.ui.panels.components.button import PanelButton
from lib.ui.panels.components.button_group import PanelButtonGroup
from lib.ui.panels.components.spacer import SpacerComponent
from lib.ui.panels.components.text import PanelText
from lib.ui.panels.components.text_input import PanelTextInput
from lib.ui.panels.components.title import TitleComponent
from lib.ui.panels.core.panel_content import PanelContent
from lib.util.events.listener import Listener
from lib.util.events.observable import Observable


class RadarDataPanel(PanelContent):
    def __init__(self, ctx: UIContext, state: AppState, events: AppEvents) -> None:
        super().__init__(ctx, state, events)

        self.listener = Listener()

        self.ctx = ctx
        self.events = events
        self.state = state

        self.latestSelected = Observable[bool](state.latest.value)

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

        self.listener.listen(
            events.ui.modals.stationSelected, self.radarInput.input.setText
        )

        self.radarName = self.addComponent(
            PanelText(
                root=self.root,
                ctx=ctx,
                text="",
            )
        )
        self.updateRadarName(state.station.value)
        self.listener.listen(self.radarInput.input.onChange, self.updateRadarName)

        self.addComponent(SpacerComponent(self.root))

        stationSearchButton = self.addComponent(
            PanelButton(self.root, ctx, "Find Radar Station")
        )

        self.listener.listen(
            stationSearchButton.button.onClick, events.ui.modals.stationSearch.send
        )

        self.addComponent(SpacerComponent(self.root))

        self.addComponent(TitleComponent(self.root, ctx, "Date and Time"))

        self.addComponent(
            PanelButtonGroup(
                self.root,
                ctx,
                self.latestSelected,
                [
                    ("Latest", True),
                    ("Historical", False),
                ],
            )
        )

        self.timeSpacer = self.addComponent(SpacerComponent(self.root))

        self.timeDescription = self.addComponent(
            PanelText(
                self.root,
                ctx,
                "Date and time format can be changed\nin Settings.",
            )
        )

        self.yearSpacer = self.addComponent(SpacerComponent(self.root))

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

        self.framesInput = self.addComponent(
            PanelTextInput(
                self.root,
                ctx,
                events,
                "Number of Frames:",
                str(state.frames.value),
                UIConstants.panelContentWidth / 4,
                validationText="1-100",
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

        self.listener.listen(loadDataButton.button.onClick, lambda _: self.search())

        self.updateInputsForLatest()
        self.listener.listen(state.latest, self.latestSelected.setValue)
        self.listener.listen(
            self.latestSelected, lambda _: self.updateInputsForLatest()
        )

    def updateInputsForLatest(self) -> None:
        self.timeSpacer.setHidden(self.latestSelected.value)
        self.timeDescription.setHidden(self.latestSelected.value)
        self.yearSpacer.setHidden(self.latestSelected.value)
        self.yearInput.setHidden(self.latestSelected.value)
        self.monthInput.setHidden(self.latestSelected.value)
        self.dayInput.setHidden(self.latestSelected.value)
        self.timeInput.setHidden(self.latestSelected.value)

        focusableItems: List[Focusable] = []
        focusableItems.append(self.radarInput.input)

        if not self.latestSelected.value:
            focusableItems.append(self.yearInput.input)
            focusableItems.append(self.monthInput.input)
            focusableItems.append(self.dayInput.input)
            focusableItems.append(self.timeInput.input)

        focusableItems.append(self.framesInput.input)

        self.setupFocusLoop(focusableItems)

    def updateRadarName(self, radar: str) -> None:
        radarStation = self.ctx.appContext.services.nws.getStation(radar)

        if not radarStation:
            self.radarName.setHidden(True)
            self.radarInput.setValid(False)
            return

        self.radarName.setHidden(False)
        self.radarInput.setValid(True)
        self.radarName.updateText(radarStation.name)

    def resetValidation(self) -> None:
        self.radarInput.setValid(True)
        self.yearInput.setValid(True)
        self.monthInput.setValid(True)
        self.dayInput.setValid(True)
        self.timeInput.setValid(True)
        self.framesInput.setValid(True)

    def search(self) -> None:
        valid = True

        self.resetValidation()

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

        # If all the datetime inputs are valid so far, perform this check
        if valid:
            try:
                datetime.datetime(year=year, month=month, day=day)
            except ValueError:
                valid = False
                self.dayInput.setValid(False)

        # The above updates validation on the datetime controls, but override
        # that if we are latest
        if self.latestSelected.value:
            valid = True

        radar = self.radarInput.input.entry.get()
        if radar not in self.ctx.appContext.services.nws.radarStations:
            valid = False
            self.radarInput.setValid(False)

        try:
            frames = int(self.framesInput.input.entry.get())
            if frames < 1 or frames > 100:
                raise ValueError("Invalid frames value")
        except ValueError:
            valid = False
            self.framesInput.setValid(False)

        if not valid:
            return

        timeQuery: TimeQuery | None = None
        if not self.latestSelected.value:
            timeQuery = TimeQuery(
                year=year,
                month=month,
                day=day,
                time=time,
            )

        query = DataQuery(
            radar=radar,
            frames=frames,
            time=timeQuery,
        )

        self.events.requestData.send(query)

    def validateTime(self, time: str) -> None:
        parts = time.split(" ")
        if self.state.use24HourTime():
            if len(parts) != 1:
                raise ValueError("Time should not have AM or PM")
        else:
            if len(parts) != 2:
                raise ValueError("Time should include AM or PM")
            ampm = parts[1]
            if ampm.lower() not in ("am", "pm"):
                raise ValueError("Time should include AM or PM")

        parts = parts[0].split(":")
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

        if self.state.use24HourTime():
            if hourInt < 1 or hourInt > 24:
                raise ValueError("Hour invalid")
        else:
            if hourInt < 1 or hourInt > 12:
                raise ValueError("Hour invalid")

    def validateYear(self, year: str) -> bool:
        try:
            yearInt = int(year)
        except ValueError:
            return False

        return 1991 <= yearInt

    def headerText(self) -> str:
        return "Radar Data"

    def destroy(self) -> None:
        super().destroy()

        self.listener.destroy()
