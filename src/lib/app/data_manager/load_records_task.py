import datetime
from typing import Callable, List

from lib.app.task.task import AbstractTask
from lib.app.time.util import TimeUtil
from lib.model.data_query import DataQuery
from lib.model.record import Record
from lib.services.radar.radar_service import RadarService


class LoadRecordsTask(AbstractTask):
    def __init__(
        self,
        radarService: RadarService,
        timeUtil: TimeUtil,
        dataQuery: DataQuery,
        onRecordsReceived: Callable[[List[Record]], None],
    ) -> None:
        super().__init__()

        self.radarService = radarService
        self.timeUtil = timeUtil
        self.dataQuery = dataQuery

        self.resultRecords: List[Record] = []
        self.onRecordsReceived = onRecordsReceived

        self.readyForProcessing()

    def doProcessing(self) -> None:
        loopEnd = self.timeUtil.getQueryTime(self.dataQuery.time)
        loopStart = loopEnd - datetime.timedelta(minutes=self.dataQuery.minutes)
        self.resultRecords = self.radarService.search(
            self.dataQuery.radar,
            loopStart,
            loopEnd,
            priorRecords=2,
        )

    def doPostProcessing(self) -> None:
        self.onRecordsReceived(self.resultRecords)

    def name(self) -> str:
        return "load records"
