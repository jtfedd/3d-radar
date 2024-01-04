import datetime
from zoneinfo import ZoneInfo

from timezonefinder import TimezoneFinder

from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.model.geo_point import GeoPoint
from lib.model.time_mode import TimeMode
from lib.services.services import Services
from lib.util.events.listener import Listener


class TimeUtil(Listener):
    def __init__(self, state: AppState, events: AppEvents, services: Services):
        super().__init__()

        self.state = state
        self.services = services
        self.events = events

        self.tf = TimezoneFinder()

        self.timezone = self.resolveTimezone()

        self.listen(state.timeMode, lambda _: self.updateTimezone())
        self.listen(state.timeZone, lambda _: self.updateTimezone())
        self.listen(state.station, lambda _: self.updateTimezone())
        self.listen(state.timeFormat, lambda _: events.timeFormatChanged.send(None))

    def updateTimezone(self) -> None:
        self.timezone = self.resolveTimezone()
        self.events.timeFormatChanged.send(None)

    def resolveTimezone(self) -> datetime.tzinfo:
        if self.state.timeMode.value == TimeMode.UTC:
            return datetime.timezone.utc

        if self.state.timeMode.value == TimeMode.RADAR:
            station = self.services.nws.getStation(self.state.station.value)
            if not station:
                raise ValueError(
                    "Unable to resolve station " + self.state.station.value
                )

            tz = self.findTimezone(station.geoPoint)
            if not tz:
                raise ValueError(
                    "Unable to resolve timezone for " + self.state.station.value
                )

            return ZoneInfo(tz)

        if self.state.timeMode.value == TimeMode.CUSTOM:
            return ZoneInfo(self.state.timeZone.value)

        raise ValueError("Unknown time mode: " + self.state.timeMode.value)

    def getQueryTime(self) -> datetime.datetime:
        if self.state.latest.value:
            return datetime.datetime.now(tz=datetime.UTC)

        year = self.state.year.value
        month = self.state.month.value
        day = self.state.day.value
        time = self.state.time.value

        if not self.state.use24HourTime():
            parts = time.split(" ")
            time = parts[0]
            ampm = parts[1].lower()

        hour = int(time.split(":")[0])
        minute = int(time.split(":")[1])

        if not self.state.use24HourTime():
            if ampm == "pm":
                hour += 12

        return datetime.datetime(
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
            second=59,
            tzinfo=self.timezone,
        )

    def getDateFormatStr(self, capitalizeMonth: bool) -> str:
        if capitalizeMonth:
            return "%d %B %Y"
        return "%d %b %Y"

    def findTimezone(self, location: GeoPoint) -> str | None:
        return self.tf.timezone_at(lng=location.lon, lat=location.lat)

    def getTimeFormatStr(self) -> str:
        if self.state.timeMode.value == TimeMode.UTC:
            return "%H:%MZ"

        if self.state.timeFormat.value:
            return "%I:%M %p"

        return "%H:%M"

    def formatTime(
        self,
        time: datetime.datetime,
        sep: str = " ",
        capitalizeMonth: bool = False,
    ) -> str:
        dateFormat = self.getDateFormatStr(capitalizeMonth)
        timeFormat = self.getTimeFormatStr()

        return time.astimezone(self.timezone).strftime(dateFormat + sep + timeFormat)
