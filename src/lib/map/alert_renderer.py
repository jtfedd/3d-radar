from __future__ import annotations

from typing import Dict, List

from panda3d.core import LineSegs, NodePath, PandaNode, Vec4

from lib.app.state import AppState
from lib.model.alert import Alert
from lib.model.alert_status import AlertStatus
from lib.model.alert_type import AlertType
from lib.model.geo_point import GeoPoint
from lib.ui.core.colors import UIColors
from lib.util.events.listener import Listener

from .util import toGlobe


class AlertRenderer(Listener):
    def __init__(
        self,
        root: NodePath[PandaNode],
        state: AppState,
        alertType: AlertType,
    ) -> None:
        super().__init__()

        self.root = root
        self.state = state
        self.alertType = alertType

        self.alerts: Dict[int, NodePath[PandaNode]] = {}

        self.renderAlerts()
        self.listen(state.alerts, lambda _: self.renderAlerts())

    def renderAlerts(self) -> None:
        payload = self.state.alerts.value
        if payload.status != AlertStatus.LOADED or self.alertType not in payload.alerts:
            self.clearAlerts()
            return

        alerts = payload.alerts[self.alertType]

        toKeep = {}

        for alert in alerts:
            alertHash = self.hashBoundary(alert.boundary)
            toKeep[alertHash] = True
            if alertHash not in self.alerts:
                self.alerts[alertHash] = self.drawAlert(alert)

        toDelete = [key for key in self.alerts if key not in toKeep]

        for key in toDelete:
            alertToRemove = self.alerts.pop(key)
            alertToRemove.removeNode()

    def hashBoundary(self, boundary: List[List[GeoPoint]]) -> int:
        loopHashes = []

        for loop in boundary:
            loopHashes.append(hash(tuple(loop)))

        return hash(tuple(loopHashes))

    def drawAlert(self, alert: Alert) -> NodePath[PandaNode]:
        lineSegs = LineSegs()

        for loop in alert.boundary:
            self.drawLoop(loop, lineSegs)

        np = NodePath(lineSegs.create())
        np.reparentTo(self.root)
        np.setColorScale(self.getColor())
        return np

    def drawLoop(self, loop: List[GeoPoint], lineSegs: LineSegs) -> None:
        if len(loop) < 4:
            return

        lineSegs.moveTo(toGlobe(loop[0]))
        for point in loop:
            lineSegs.drawTo(toGlobe(point))

    def getColor(self) -> Vec4:
        if self.alertType == AlertType.TORNADO_WARNING:
            return UIColors.RED
        if self.alertType == AlertType.SEVERE_THUNDERSTORM_WARNING:
            return UIColors.ORANGE

        return UIColors.WHITE

    def clearAlerts(self) -> None:
        toDelete = list(self.alerts)

        for key in toDelete:
            alert = self.alerts.pop(key)
            alert.removeNode()

    def destroy(self) -> None:
        super().destroy()

        self.clearAlerts()
