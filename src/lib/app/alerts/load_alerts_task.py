from typing import Callable, List

from lib.app.task.task import AbstractTask
from lib.model.alert import Alert
from lib.model.alert_type import AlertType
from lib.services.nws.nws_service import NWSService


class LoadAlertsTask(AbstractTask):
    def __init__(
        self,
        nwsService: NWSService,
        alertType: AlertType,
        onAlertsLoaded: Callable[[AlertType, List[Alert] | None], None],
    ) -> None:
        super().__init__()

        self.nwsService = nwsService
        self.alertType = alertType

        self.resultAlerts: List[Alert] | None = []
        self.onAlertsLoaded = onAlertsLoaded

        self.readyForProcessing()

    def doProcessing(self) -> None:
        self.resultAlerts = self.nwsService.getAlerts(self.alertType)

    def doPostProcessing(self) -> None:
        self.onAlertsLoaded(self.alertType, self.resultAlerts)

    def name(self) -> str:
        return "load alerts " + str(self.alertType)
