from typing import Dict, List

from direct.task.Task import Task

from lib.app.context import AppContext
from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.model.alert import Alert
from lib.model.alert_payload import AlertPayload
from lib.model.alert_status import AlertStatus
from lib.model.alert_type import AlertType
from lib.util.events.listener import Listener

from .loading_task import LoadingTask


class AlertManager(Listener):
    UPDATE_INTERVAL = 30

    def __init__(self, ctx: AppContext, state: AppState, events: AppEvents):
        super().__init__()

        self.ctx = ctx
        self.state = state
        self.events = events

        self.monitoring = False
        self.nextUpdate = 0.0
        self.lastUpdate = 0.0

        self.loadingTask: LoadingTask | None = None

        self.updateTask = ctx.base.taskMgr.add(self.update, "alerts-update")

        self.handleMonitoringChange(state.latest.value)
        self.listen(state.latest, self.handleMonitoringChange)

    def update(self, task: Task) -> int:
        dt = task.time - self.lastUpdate
        self.lastUpdate = task.time

        if not self.monitoring:
            return task.cont

        self.nextUpdate -= dt
        if self.nextUpdate <= 0:
            self.loadAlerts()
            self.nextUpdate = AlertManager.UPDATE_INTERVAL

        return task.cont

    def loadAlerts(self) -> None:
        if not self.monitoring:
            self.state.alerts.setValue(
                AlertPayload(status=AlertStatus.READY, alerts={})
            )
            return

        if self.loadingTask is not None:
            self.loadingTask.cancel()

        self.loadingTask = LoadingTask(self.ctx, self.onAlertsLoaded)

    def onAlertsLoaded(self, alerts: Dict[AlertType, List[Alert]] | None) -> None:
        self.loadingTask = None

        if alerts is None:
            self.state.alerts.setValue(
                AlertPayload(status=AlertStatus.ERROR, alerts={})
            )
            return

        self.state.alerts.setValue(
            AlertPayload(status=AlertStatus.LOADED, alerts=alerts)
        )

    def handleMonitoringChange(self, shouldMonitor: bool) -> None:
        if shouldMonitor == self.monitoring:
            return

        self.monitoring = shouldMonitor

        self.loadAlerts()
        self.nextUpdate = AlertManager.UPDATE_INTERVAL

    def destroy(self) -> None:
        super().destroy()
        self.updateTask.cancel()
