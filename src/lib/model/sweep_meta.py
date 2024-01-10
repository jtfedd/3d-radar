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
        offset: int,
    ):
        self.elevation = elevation
        self.azFirst = azFirst
        self.azStep = azStep
        self.azCount = azCount
        self.rngFirst = rngFirst
        self.rngStep = rngStep
        self.rngCount = rngCount
        self.offset = offset
