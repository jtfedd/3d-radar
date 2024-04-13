from typing import List

from .alert_type import AlertType
from .geo_point import GeoPoint


class Alert:
    def __init__(self, alertType: AlertType, name: str, boundary: List[List[GeoPoint]]):
        self.alertType = alertType
        self.name = name
        self.boundary = boundary
