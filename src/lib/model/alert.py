from .alert_type import AlertType


class Alert:
    def __init__(self, alertType: AlertType, name: str):
        self.alertType = alertType
        self.name = name
