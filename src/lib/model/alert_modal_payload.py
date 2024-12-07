from lib.model.alert import Alert


class AlertModalPayload:
    def __init__(self, alert: Alert, back: bool = True):
        self.alert = alert
        self.back = back
