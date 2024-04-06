from typing import Dict, List

from .alert import Alert
from .alert_status import AlertStatus
from .alert_type import AlertType


class AlertPayload:
    def __init__(self, status: AlertStatus, alerts: Dict[AlertType, List[Alert]]):
        self.status = status
        self.alerts = alerts
