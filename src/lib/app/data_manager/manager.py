from collections import defaultdict
from typing import Dict, List

from direct.task.Task import Task

from lib.app.context import AppContext
from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.model.data_query import DataQuery
from lib.model.record import Record
from lib.model.scan import Scan
from lib.model.time_query import TimeQuery
from lib.util.events.listener import Listener

from .loading_task import LoadingTask


class DataManager(Listener):
    REFRESH_INTERVAL = 60

    def __init__(
        self,
        ctx: AppContext,
        state: AppState,
        events: AppEvents,
    ) -> None:
        super().__init__()

        self.cache: Dict[str, Scan] = {}

        self.ctx = ctx
        self.state = state
        self.events = events

        self.loadingTask: LoadingTask | None = None

        self.load(self.dataQueryFromCurrentState())
        self.listen(events.requestData, self.load)
        self.listen(events.refreshData, lambda _: self.refresh())

        self.refreshTimer = 0.0
        self.lastRefresh = 0.0
        self.refreshTask = ctx.base.taskMgr.add(self.updateRefresh, "refresh-data")

    def updateRefresh(self, task: Task) -> int:
        self.refreshTimer += task.time - self.lastRefresh
        self.lastRefresh = task.time

        if self.refreshTimer > self.REFRESH_INTERVAL:
            self.refresh()

        return task.cont

    def dataQueryFromCurrentState(self) -> DataQuery:
        radar = self.state.station.value
        frames = self.state.frames.value
        time: TimeQuery | None = None
        if not self.state.latest.value:
            time = TimeQuery(
                year=self.state.year.value,
                month=self.state.month.value,
                day=self.state.day.value,
                time=self.state.time.value,
            )

        return DataQuery(
            radar=radar,
            frames=frames,
            time=time,
        )

    def applyDataQueryToState(self, query: DataQuery) -> None:
        self.state.station.setValue(query.radar)
        self.state.frames.setValue(query.frames)
        self.state.latest.setValue(query.time is None)
        if query.time is not None:
            self.state.year.setValue(query.time.year)
            self.state.month.setValue(query.time.month)
            self.state.day.setValue(query.time.day)
            self.state.time.setValue(query.time.time)

    def load(self, dataQuery: DataQuery) -> None:
        self.state.loadingData.setValue(True)
        self.refreshTimer = 0

        if self.loadingTask is not None:
            self.loadingTask.cancel()

        self.loadingTask = LoadingTask(
            self.ctx,
            dataQuery,
            lambda key: self.state.animationData.value[key],
            self.onDataLoaded,
        )

    def refresh(self) -> None:
        if not self.state.latest.value or self.loadingTask is not None:
            return

        self.load(self.dataQueryFromCurrentState())

    def onDataLoaded(
        self, query: DataQuery, records: List[Record], scans: Dict[str, Scan]
    ) -> None:
        self.refreshTimer = 0
        self.state.loadingData.setValue(False)

        self.loadingTask = None
        self.applyDataQueryToState(query)
        self.state.animationData.setValue(defaultdict(lambda: None, scans))
        self.state.animationRecords.setValue(records)

    def destroy(self) -> None:
        super().destroy()

        self.refreshTask.cancel()
