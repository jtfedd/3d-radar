import datetime


class SweepMeta:
    def __init__(
        self,
        elevation: float,
        azFirst: float,
        azStep: float,
        azCount: int,
        rngFirst: float,
        rngStep: float,
        rngCount: int,
        startTime: int,
        endTime: int,
        offset: int,
    ):
        self.elevation = elevation
        self.azFirst = azFirst
        self.azStep = azStep
        self.azCount = azCount
        self.rngFirst = rngFirst
        self.rngStep = rngStep
        self.rngCount = rngCount
        self.startTime = datetime.datetime.fromtimestamp(
            startTime,
            datetime.timezone.utc,
        )
        self.endTime = datetime.datetime.fromtimestamp(
            endTime,
            datetime.timezone.utc,
        )
        self.offset = offset
