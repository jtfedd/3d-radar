import datetime

from timezonefinder import TimezoneFinder

from lib.app.state import AppState
from lib.model.geo_point import GeoPoint


class TimeUtil:
    def __init__(self, state: AppState):
        self.state = state
        self.tf = TimezoneFinder()

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
            tzinfo=datetime.timezone.utc,
        )

    def getDateFormatStr(self, capitalizeMonth: bool) -> str:
        if capitalizeMonth:
            return "%d %B %Y"
        return "%d %b %Y"

    def findTimezone(self, location: GeoPoint) -> str | None:
        return self.tf.timezone_at(lng=location.lon, lat=location.lat)

    def getTimeFormatStr(self) -> str:
        return "%I:%M %p"

    def formatTime(
        self,
        time: datetime.datetime,
        sep: str = " ",
        capitalizeMonth: bool = False,
    ) -> str:
        dateFormat = self.getDateFormatStr(capitalizeMonth)
        timeFormat = self.getTimeFormatStr()

        return time.strftime(dateFormat + sep + timeFormat)
