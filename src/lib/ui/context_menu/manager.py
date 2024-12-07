from typing import List

from lib.app.context import AppContext
from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.geometry.polygon_contains import polygonContains
from lib.map.constants import RADAR_RANGE
from lib.model.alert import Alert
from lib.model.alert_status import AlertStatus
from lib.model.alert_type import AlertType
from lib.model.context_menu_payload import ContextMenuPayload
from lib.model.geo_point import GeoPoint
from lib.ui.context_menu.context_menu import ContextMenu
from lib.ui.context_menu.context_menu_group import ContextMenuGroup
from lib.ui.context_menu.context_menu_item import ContextMenuItem
from lib.ui.context_menu.stations.station_item import StationItem
from lib.ui.context_menu.warnings.warning_item import WarningItem
from lib.util.events.listener import Listener


class ContextMenuManager(Listener):
    def __init__(self, ctx: AppContext, state: AppState, events: AppEvents):
        super().__init__()
        self.ctx = ctx
        self.state = state
        self.events = events

        self.contextMenu: ContextMenu | None = None

        self.listen(events.ui.requestContextMenu, self.openContextMenu)
        self.listen(events.ui.closeContextMenu, lambda _: self.closeContextMenu())
        self.listen(
            events.input.leftMouse,
            lambda down: self.closeContextMenu() if down else None,
        )
        self.listen(
            events.input.rightMouse,
            lambda down: self.closeContextMenu() if down else None,
        )
        self.listen(
            events.input.leftMouseRaw,
            lambda down: self.closeContextMenu(checkBounds=True) if down else None,
        )
        self.listen(
            events.input.rightMouseRaw,
            lambda down: self.closeContextMenu(checkBounds=True) if down else None,
        )

    def openContextMenu(self, payload: ContextMenuPayload) -> None:
        if self.contextMenu is not None:
            self.closeContextMenu()

        groups = self.getContextMenuGroupsForPoint(payload.geoPoint)
        if len(groups) > 0:
            self.contextMenu = ContextMenu(
                self.ctx,
                self.state,
                self.events,
                payload.screenPoint,
                groups,
            )

    def closeContextMenu(self, checkBounds: bool = False) -> None:
        if self.contextMenu is not None:
            if checkBounds and self.contextMenu.checkMouseInBounds():
                return

            self.contextMenu.destroy()
            self.contextMenu = None

    def getContextMenuGroupsForPoint(
        self, geoPoint: GeoPoint
    ) -> List[ContextMenuGroup]:
        groups: List[ContextMenuGroup] = []

        warningsGroup = self.getWarningsGroupForPoint(geoPoint)
        if warningsGroup is not None:
            groups.append(warningsGroup)

        stationsGroup = self.getStationsGroupForPoint(geoPoint)
        if stationsGroup is not None:
            groups.append(stationsGroup)

        return groups

    def getWarningsGroupForPoint(self, geoPoint: GeoPoint) -> ContextMenuGroup | None:
        items: List[ContextMenuItem] = []

        alerts = self.state.alerts.getValue()
        if alerts.status == AlertStatus.LOADED:
            if AlertType.TORNADO_WARNING in alerts.alerts:
                items += self.getWarningItems(
                    geoPoint, alerts.alerts[AlertType.TORNADO_WARNING]
                )
            if AlertType.SEVERE_THUNDERSTORM_WARNING in alerts.alerts:
                items += self.getWarningItems(
                    geoPoint, alerts.alerts[AlertType.SEVERE_THUNDERSTORM_WARNING]
                )

        if len(items) > 0:
            return ContextMenuGroup(header="Active Warnings", items=items)

        return None

    def getWarningItems(
        self, geoPoint: GeoPoint, alerts: List[Alert]
    ) -> List[WarningItem]:
        if alerts is None or len(alerts) == 0:
            return []

        items: List[WarningItem] = []

        for alert in alerts:
            for ring in alert.boundary:
                if polygonContains(ring, geoPoint):
                    items.append(WarningItem(self.events, alert))
                    break

        return items

    def getStationsGroupForPoint(self, geoPoint: GeoPoint) -> ContextMenuGroup | None:
        stations = list(self.ctx.services.nws.radarStations.values())
        stations.sort(key=lambda s: s.geoPoint.dist(geoPoint))

        items: List[ContextMenuItem] = []

        i = 0
        while (
            i < 3
            and i < len(stations)
            and stations[i].geoPoint.dist(geoPoint) < RADAR_RANGE
        ):
            items.append(
                StationItem(
                    self.events,
                    self.state,
                    stations[i],
                    geoPoint,
                )
            )
            i += 1

        if len(items) > 0:
            return ContextMenuGroup(header="Nearby Radar Stations", items=items)

        return None
