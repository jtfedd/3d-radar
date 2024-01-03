import datetime

from lib.app.state import AppState


class TimeUtil:
    def __init__(self, state: AppState):
        self.state = state

    def getQueryTime(self) -> datetime.datetime:
        if self.state.latest.value:
            return datetime.datetime.now(tz=datetime.UTC)

        year = self.state.year.value
        month = self.state.month.value
        day = self.state.day.value
        time = self.state.time.value

        hour = int(time.split(":")[0])
        minute = int(time.split(":")[1])

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
