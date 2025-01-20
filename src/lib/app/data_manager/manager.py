from collections import defaultdict
from typing import Dict

from direct.task.Task import Task

from lib.app.context import AppContext
from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.model.data_query import DataQuery
from lib.model.loading_progress_payload import LoadingProgressPayload
from lib.model.scan import Scan
from lib.util.events.listener import Listener
from lib.util.state import applyDataQueryToState, dataQueryFromState

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

        initialQuery = dataQueryFromState(state)
        self.onDataLoaded(initialQuery, {})
        self.onDataRequested(initialQuery)
        self.listen(events.requestData, self.onDataRequested)
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

    def onDataRequested(self, dataQuery: DataQuery) -> None:
        self.load(dataQuery)
        if self.loadingTask is not None:
            self.events.ui.modals.loadingProgress.send(
                LoadingProgressPayload(
                    self.loadingTask.progress,
                    self.loadingTask.onComplete,
                    self.loadingTask.cancel,
                )
            )

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
            self.onLoadCancelled,
        )

    def refresh(self) -> None:
        if not self.state.latest.value or self.loadingTask is not None:
            return

        self.load(dataQueryFromState(self.state))

    def onLoadCancelled(self) -> None:
        self.refreshTimer = 0
        self.state.loadingData.setValue(False)
        self.loadingTask = None

    def onDataLoaded(self, query: DataQuery, scans: Dict[str, Scan]) -> None:
        self.refreshTimer = 0
        self.state.loadingData.setValue(False)
        self.loadingTask = None

        applyDataQueryToState(self.state, query)
        self.state.animationData.setValue(
            defaultdict(lambda: None, scans),
            forceSend=True,
        )

        animationTimestamp = int(
            round(
                (
                    self.ctx.timeUtil.getQueryTime(query.time) or query.queryTimestamp
                ).timestamp()
            )
        )
        self.state.animationBounds.setValue(
            (animationTimestamp - (60 * query.minutes), animationTimestamp)
        )
        self.state.animationTime.setValue(animationTimestamp)

    def destroy(self) -> None:
        super().destroy()

        self.refreshTask.cancel()
        if self.loadingTask is not None:
            self.loadingTask.cancel()
