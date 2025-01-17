import datetime
from typing import List

import pynexrad

from lib.app.logging import newLogger
from lib.model.record import Record
from lib.model.scan import Scan
from lib.model.sweep import Sweep


def convertSweep(sweep: pynexrad.Sweep) -> Sweep:
    return Sweep(
        sweep.elevation,
        sweep.az_first,
        sweep.az_step,
        sweep.az_count,
        sweep.range_first,
        sweep.range_step,
        sweep.range_count,
        sweep.start_time,
        sweep.end_time,
        bytearray(sweep.data),
    )


def convertSweeps(sweeps: List[pynexrad.Sweep]) -> List[Sweep]:
    return [convertSweep(sweep) for sweep in sweeps]


def convertLevel2File(record: Record, file: pynexrad.Level2File) -> Scan:
    return Scan(
        record,
        convertSweeps(file.reflectivity),
        convertSweeps(file.velocity),
    )


class RadarProvider:
    def __init__(self) -> None:
        self.log = newLogger("radar_provider")

    def load(self, record: Record) -> Scan:
        key = record.awsKey()

        self.log.info(f"Fetching from s3: {key}")

        level2File = pynexrad.download_nexrad_file(key)

        self.log.info(f"Post-processing {key}")
        return convertLevel2File(record, level2File)

    def search(
        self,
        radar: str,
        loopStart: datetime.datetime,
        loopEnd: datetime.datetime,
        priorRecords: int = 0,
    ) -> List[Record]:
        searchStart = loopStart

        # Search a maximum of one hour before to find prior records
        if priorRecords > 0:
            searchStart = loopStart - datetime.timedelta(hours=1)

        searchStart = searchStart.astimezone(datetime.timezone.utc)
        loopStart = loopStart.astimezone(datetime.timezone.utc)
        searchTime = loopEnd.astimezone(datetime.timezone.utc)

        # Get records from the day of the search end
        records = self.getScans(
            radar,
            searchTime.year,
            searchTime.month,
            searchTime.day,
        )

        # If the search start is on the previous day, load records from that day as well
        if searchStart.day != searchTime.day:
            records.extend(
                self.getScans(
                    radar,
                    searchStart.year,
                    searchStart.month,
                    searchStart.day,
                )
            )

        # Records between the search start and the start of the loop
        preceedingRecords = list(
            filter(lambda r: r.time >= searchStart and r.time < loopStart, records)
        )

        # Records in the animation loop
        records = list(
            filter(lambda r: r.time >= loopStart and r.time <= searchTime, records)
        )

        # If we should include some prior records, include up to that many from the end
        # of the list of preceeding records
        if priorRecords > 0:
            preceedingRecords.sort(key=lambda r: r.time)

            preceedingRecords = (
                preceedingRecords[-priorRecords:]
                if len(preceedingRecords) >= priorRecords
                else preceedingRecords
            )
            records = preceedingRecords + records

        records.sort(key=lambda r: r.time)

        return records

    def getScans(self, radar: str, year: int, month: int, day: int) -> List[Record]:
        resp = pynexrad.list_records(radar, year, month, day)

        records = []

        for key in resp:
            record = Record.parse(key)
            if record:
                records.append(record)

        return records
