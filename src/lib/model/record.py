import datetime


class Record:
    def __init__(self, station: str, time: datetime.datetime):
        self.station = station
        self.time = time

    def awsKey(self) -> str:
        return self.format("{1:02}/{2:02}/{3:02}/{0}/" + self.cacheKey())

    def cacheKey(self) -> str:
        return self.format("{0}{1:02}{2:02}{3:02}_{4:02}{5:02}{6:02}")

    def format(self, fmt: str) -> str:
        return fmt.format(
            self.station,
            self.time.year,
            self.time.month,
            self.time.day,
            self.time.hour,
            self.time.minute,
            self.time.second,
        )
