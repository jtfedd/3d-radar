from typing import Callable, Dict, List

from lib.app.context import AppContext
from lib.model.alert import Alert
from lib.model.alert_type import AlertType

from .load_alerts_task import LoadAlertsTask


class LoadingTask:
    def __init__(
        self,
        ctx: AppContext,
        loadCompleteCallback: Callable[[Dict[AlertType, List[Alert]] | None], None],
    ) -> None:
        self.cancelled = False

        self.ctx = ctx
        self.loadCompleteCallback = loadCompleteCallback

        self.results: Dict[AlertType, List[Alert]] = {}

        self.tasks = [
            LoadAlertsTask(
                ctx.services.nws,
                AlertType.TORNADO_WARNING,
                self.onAlertsLoaded,
            ),
            LoadAlertsTask(
                ctx.services.nws,
                AlertType.SEVERE_THUNDERSTORM_WARNING,
                self.onAlertsLoaded,
            ),
        ]

        for task in self.tasks:
            self.ctx.taskManager.addTask(task)

    def cancel(self) -> None:
        self.cancelled = True
        for task in self.tasks:
            task.cancel()

    def onAlertsLoaded(self, alertType: AlertType, alerts: List[Alert] | None) -> None:
        if self.cancelled:
            return

        if alerts is None:
            self.cancel()
            self.loadCompleteCallback(None)
            return

        self.results[alertType] = alerts

        if len(self.results) == len(self.tasks):
            self.loadCompleteCallback(self.results)
