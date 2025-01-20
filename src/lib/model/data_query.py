import datetime

from .time_query import TimeQuery


class DataQuery:
    def __init__(
        self,
        radar: str,
        minutes: int,
        time: TimeQuery | None,
    ):
        self.radar = radar
        self.minutes = minutes
        self.time = time

        self.queryTimestamp = datetime.datetime.now(tz=datetime.UTC)
