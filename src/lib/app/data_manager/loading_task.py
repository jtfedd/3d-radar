from typing import Callable, Dict, List

from lib.app.context import AppContext
from lib.model.data_query import DataQuery
from lib.model.record import Record
from lib.model.scan import Scan

from .load_data_task import LoadDataTask
from .load_records_task import LoadRecordsTask


class LoadingTask:
    def __init__(
        self,
        ctx: AppContext,
        dataQuery: DataQuery,
        getCachedScan: Callable[[str], Scan | None],
        loadCompleteCallback: Callable[
            [DataQuery, List[Record], Dict[str, Scan]], None
        ],
    ) -> None:
        self.cancelled = False

        self.ctx = ctx
        self.getCachedScan = getCachedScan
        self.loadCompleteCallback = loadCompleteCallback
        self.dataQuery = dataQuery

        self.loadRecordsTask = LoadRecordsTask(
            self.ctx.services.radar,
            self.ctx.timeUtil,
            dataQuery,
            self.onListRecordsComplete,
        )
        self.ctx.taskManager.addTask(self.loadRecordsTask)

        self.loadDataTasks: List[LoadDataTask] = []

        self.resultRecords: List[Record] = []
        self.resultScans: Dict[str, Scan] = {}

    def cancel(self) -> None:
        self.cancelled = True
        self.loadRecordsTask.cancel()
        for task in self.loadDataTasks:
            task.cancel()

    def onListRecordsComplete(self, records: List[Record]) -> None:
        if self.cancelled:
            return

        self.resultRecords = records

        for record in records:
            cachedScan = self.getCachedScan(record.key())
            if cachedScan is not None:
                self.resultScans[record.key()] = cachedScan
                continue

            loadDataTask = LoadDataTask(
                self.ctx.services.radar,
                record,
                self.onLoadFileComplete,
            )

            self.ctx.taskManager.addTask(loadDataTask)
            self.loadDataTasks.append(loadDataTask)

    def onLoadFileComplete(self, scan: Scan) -> None:
        if self.cancelled:
            return

        self.resultScans[scan.record.key()] = scan

        if len(self.resultScans) == len(self.loadDataTasks):
            self.onLoadComplete()

    def onLoadComplete(self) -> None:
        if self.cancelled:
            return

        self.loadCompleteCallback(self.dataQuery, self.resultRecords, self.resultScans)
