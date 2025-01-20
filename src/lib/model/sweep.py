from typing import Self


class Sweep:
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
        data: bytes,
    ):
        self.elevation = elevation
        self.azFirst = azFirst
        self.azStep = azStep
        self.azCount = azCount
        self.rngFirst = rngFirst
        self.rngStep = rngStep
        self.rngCount = rngCount
        self.startTime = startTime
        self.endTime = endTime
        self.data = data

    @classmethod
    def empty(cls, elevation: float) -> Self:
        return cls(
            elevation=elevation,
            azFirst=0,
            azStep=0,
            azCount=0,
            rngFirst=0,
            rngStep=0,
            rngCount=0,
            startTime=0,
            endTime=0,
            data=bytes(),
        )
