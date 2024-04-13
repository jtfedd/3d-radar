from direct.task.Task import Task

from lib.app.context import AppContext
from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.model.alert_payload import AlertPayload
from lib.model.alert_status import AlertStatus
from lib.util.events.listener import Listener


class AlertManager(Listener):
    UPDATE_INTERVAL = 5

    def __init__(self, ctx: AppContext, state: AppState, events: AppEvents):
        super().__init__()

        self.ctx = ctx
        self.state = state
        self.events = events

        self.monitoring = False
        self.nextUpdate = 0.0
        self.lastUpdate = 0.0

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

        alerts = self.ctx.services.nws.getAlerts()
        if alerts is not None:
            self.state.alerts.setValue(
                AlertPayload(status=AlertStatus.LOADED, alerts=alerts)
            )
            return

        self.state.alerts.setValue(AlertPayload(status=AlertStatus.ERROR, alerts={}))

    def handleMonitoringChange(self, shouldMonitor: bool) -> None:
        if shouldMonitor == self.monitoring:
            return

        self.monitoring = shouldMonitor

        self.loadAlerts()
        self.nextUpdate = AlertManager.UPDATE_INTERVAL

    def destroy(self) -> None:
        super().destroy()
        self.updateTask.cancel()
