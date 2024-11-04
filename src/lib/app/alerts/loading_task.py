from typing import Callable, Dict, List

from lib.app.context import AppContext
from lib.app.task.task_status import TaskStatus
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
        self.loadCompleteCallback(None)

    def onAlertsLoaded(self, alertType: AlertType, alerts: List[Alert] | None) -> None:
        if self.cancelled:
            return

        if alerts is None:
            self.cancel()
            return

        self.results[alertType] = alerts

        complete = True
        for task in self.tasks:
            if not task.isActive():
                if task.getStatus() != TaskStatus.COMPLETE:
                    self.cancel()
                    return
            else:
                complete = False
                break

        if complete:
            self.loadCompleteCallback(self.results)
