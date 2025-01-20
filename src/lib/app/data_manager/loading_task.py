from typing import Callable, Dict, List

from lib.app.context import AppContext
from lib.model.data_query import DataQuery
from lib.model.record import Record
from lib.model.scan import Scan
from lib.util.events.event_dispatcher import EventDispatcher
from lib.util.events.observable import Observable

from .load_data_task import LoadDataTask
from .load_records_task import LoadRecordsTask


class LoadingTask:
    def __init__(
        self,
        ctx: AppContext,
        dataQuery: DataQuery,
        getCachedScan: Callable[[str], Scan | None],
        loadCompleteCallback: Callable[[DataQuery, Dict[str, Scan]], None],
        loadCancelledCallback: Callable[[], None],
    ) -> None:
        self.cancelled = False
        self.onComplete = EventDispatcher[None]()

        self.progress = Observable[float](0.0)

        self.ctx = ctx
        self.getCachedScan = getCachedScan
        self.loadCompleteCallback = loadCompleteCallback
        self.loadCancelledCallback = loadCancelledCallback
        self.dataQuery = dataQuery

        self.loadRecordsTask = LoadRecordsTask(
            self.ctx.services.radar,
            self.ctx.timeUtil,
            dataQuery,
            self.onListRecordsComplete,
        )
        self.ctx.taskManager.addTask(self.loadRecordsTask)

        self.tasksComplete = 0
        self.loadDataTasks: List[LoadDataTask] = []

        self.resultRecords: List[Record] = []
        self.resultScans: Dict[str, Scan] = {}

    def updateProgress(self) -> None:
        if len(self.loadDataTasks) == 0:
            self.progress.setValue(0.0)
            return

        self.progress.setValue(self.tasksComplete / len(self.loadDataTasks))

    def cancel(self) -> None:
        if self.cancelled:
            return

        self.cancelled = True
        self.onComplete.send(None)
        self.loadRecordsTask.cancel()
        for task in self.loadDataTasks:
            task.cancel()

        self.loadCancelledCallback()

    def onListRecordsComplete(self, records: List[Record]) -> None:
        if self.cancelled:
            return

        self.resultRecords = records

        for record in records:
            cachedScan = self.getCachedScan(record.key())
            if cachedScan is not None:
                self.addResultScan(cachedScan)
                continue

            loadDataTask = LoadDataTask(
                self.ctx.services.radar,
                record,
                self.onLoadFileComplete,
            )

            self.ctx.taskManager.addTask(loadDataTask)
            self.loadDataTasks.append(loadDataTask)

        self.updateProgress()

    def onLoadFileComplete(self, scan: Scan) -> None:
        self.tasksComplete += 1
        self.updateProgress()

        self.addResultScan(scan)

    def addResultScan(self, scan: Scan) -> None:
        if self.cancelled:
            return

        self.resultScans[scan.record.key()] = scan

        if len(self.resultScans) == len(self.resultRecords):
            self.onLoadComplete()

    def onLoadComplete(self) -> None:
        if self.cancelled:
            return

        self.onComplete.send(None)

        self.loadCompleteCallback(self.dataQuery, self.resultScans)
