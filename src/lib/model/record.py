import datetime
from typing import Self


class Record:
    FILE_FMT = "{0}{1:02}{2:02}{3:02}_{4:02}{5:02}{6:02}"

    def __init__(self, station: str, time: datetime.datetime, extension: str = "V06"):
        self.station = station
        self.time = time
        self.extension = extension

    def awsKey(self) -> str:
        return self.format(self.key() + "_" + self.extension)

    def key(self) -> str:
        return self.format(self.FILE_FMT)

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

    @classmethod
    def parse(cls, awsKey: str) -> Self | None:
        fileParts = awsKey.split("_")
        if len(fileParts) != 3:
            return None

        stationDate = fileParts[0]
        time = fileParts[1]
        extension = fileParts[2]

        if len(stationDate) != 12:
            return None
        if len(time) != 6:
            return None

        station = stationDate[0:4]

        try:
            year = int(stationDate[4:8])
            month = int(stationDate[8:10])
            day = int(stationDate[10:12])
        except ValueError:
            return None

        try:
            hour = int(time[0:2])
            minute = int(time[2:4])
            second = int(time[4:6])
        except ValueError:
            return None

        return cls(
            station,
            datetime.datetime(
                year,
                month,
                day,
                hour,
                minute,
                second,
                tzinfo=datetime.timezone.utc,
            ),
            extension=extension,
        )
