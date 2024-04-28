from typing import Dict, List

from .alert import Alert
from .alert_status import AlertStatus
from .alert_type import AlertType


class AlertPayload:
    def __init__(self, status: AlertStatus, alerts: Dict[AlertType, List[Alert]]):
        self.status = status
        self.alerts = alerts

        if AlertType.TORNADO_WARNING not in self.alerts:
            self.alerts[AlertType.TORNADO_WARNING] = []
        if AlertType.SEVERE_THUNDERSTORM_WARNING not in self.alerts:
            self.alerts[AlertType.SEVERE_THUNDERSTORM_WARNING] = []

        self._count = sum(len(a) for a in self.alerts.values())

    def count(self) -> int:
        return self._count
