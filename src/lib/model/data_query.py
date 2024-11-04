from .time_query import TimeQuery


class DataQuery:
    def __init__(
        self,
        radar: str,
        frames: int,
        time: TimeQuery | None,
    ):
        self.radar = radar
        self.frames = frames
        self.time = time
