import datetime
from typing import Self


class Record:
    PREFIX_FMT = "{1:02}/{2:02}/{3:02}/{0}/"
    FILE_FMT = "{0}{1:02}{2:02}{3:02}_{4:02}{5:02}{6:02}"

    def __init__(self, station: str, time: datetime.datetime, extension: str = "V06"):
        self.station = station
        self.time = time
        self.extension = extension

    def awsKey(self) -> str:
        return self.format(self.awsPrefix() + self.cacheKey() + "_" + self.extension)

    def awsPrefix(self) -> str:
        return self.format(self.PREFIX_FMT)

    def cacheKey(self) -> str:
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
        pathParts = awsKey.split("/")
        if len(pathParts) != 5:
            return None

        station = pathParts[3]

        try:
            year = int(pathParts[0])
            month = int(pathParts[1])
            day = int(pathParts[2])
        except ValueError:
            return None

        fileParts = pathParts[4].split("_")
        if len(fileParts) != 3:
            return None

        stationDate = fileParts[0]
        time = fileParts[1]
        extension = fileParts[2]

        check = f"{station}{year:02}{month:02}{day:02}"

        if stationDate != check:
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
