from typing import List

from lib.app.context import AppContext
from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.model.alert import Alert
from lib.model.alert_modal_payload import AlertModalPayload
from lib.model.alert_status import AlertStatus
from lib.model.alert_type import AlertType
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.components.scrollable_panel import ScrollablePanel
from lib.ui.core.components.text import Text
from lib.ui.core.constants import UIConstants
from lib.ui.core.layers import UILayer
from lib.util.events.event_subscription import EventSubscription
from lib.util.events.listener import Listener
from lib.util.optional import unwrap

from ..core.modal import Modal
from ..core.title import ModalTitle
from .alert_button import AlertButton


class AlertsModal(Modal):
    def __init__(self, ctx: AppContext, state: AppState, events: AppEvents):
        super().__init__(
            ctx,
            events,
            UIConstants.alertsModalWidth,
            UIConstants.alertsModalHeight,
            closeButton=True,
        )

        self.ctx = ctx
        self.state = state
        self.appEvents = events

        self.listener = Listener()

        self.title = ModalTitle(
            ctx, self.topLeft, "Active Warnings", UIConstants.alertsModalWidth
        )

        self.text = Text(
            root=self.topLeft,
            font=ctx.fonts.regular,
            text="",
            vAlign=VAlign.CENTER,
            hAlign=HAlign.CENTER,
            y=-UIConstants.alertsModalHeight / 2,
            x=UIConstants.alertsModalWidth / 2,
            size=UIConstants.fontSizeRegular,
            layer=UILayer.MODAL_CONTENT,
        )

        self.scroll = ScrollablePanel(
            root=self.topLeft,
            ctx=ctx,
            events=events,
            y=-(self.title.height() + UIConstants.modalPadding),
            width=UIConstants.alertsModalWidth + UIConstants.modalPadding,
            hAlign=HAlign.LEFT,
            vAlign=VAlign.TOP,
            layer=UILayer.MODAL_CONTENT_INTERACTION,
            scrollbarPadding=UIConstants.modalScrollbarPadding,
        )

        self.alertButtons: List[AlertButton] = []
        self.buttonSubs: List[EventSubscription[None]] = []

        self.updateContent()
        self.listener.listen(state.alerts, lambda _: self.updateContent())
        self.listener.listen(state.station, lambda _: self.updateContent())

    def updateContent(self) -> None:
        alerts = self.state.alerts.value
        count = alerts.count()

        if alerts.status == AlertStatus.LOADED and count > 0:
            self.text.hide()
            self.scroll.show()

        else:
            self.text.show()
            self.scroll.hide()

        if alerts.status == AlertStatus.ERROR:
            self.text.updateText("Error Loading Warnings")

        if alerts.status == AlertStatus.READY or (
            alerts.status == AlertStatus.LOADED and count == 0
        ):
            self.text.updateText("No Active Warnings")

        if alerts.status == AlertStatus.LOADED and count > 0:
            self.updateAlertCards()

    def updateAlertCards(self) -> None:
        alerts = self.state.alerts.value

        for button in self.alertButtons:
            button.destroy()
        for sub in self.buttonSubs:
            sub.cancel()
        self.alertButtons.clear()
        self.buttonSubs.clear()

        torWarnings = alerts.alerts[AlertType.TORNADO_WARNING]
        svrWarnings = alerts.alerts[AlertType.SEVERE_THUNDERSTORM_WARNING]

        station = self.ctx.services.nws.getStation(self.state.station.value)
        if station:
            torWarnings.sort(key=lambda a: a.center().dist(unwrap(station).geoPoint))
            svrWarnings.sort(key=lambda a: a.center().dist(unwrap(station).geoPoint))

        allWarnings = torWarnings + svrWarnings

        top = 0.0
        for alert in allWarnings:
            button = self.createAlertButton(alert, top)

            top += button.getHeight()
            top += UIConstants.alertsButtonPadding

        self.scroll.updateFrame(
            UIConstants.alertsModalHeight
            - UIConstants.modalPadding
            - self.title.height(),
            top - UIConstants.alertsButtonPadding,
        )

    def createAlertButton(self, alert: Alert, top: float) -> AlertButton:
        button = AlertButton(
            self.ctx,
            self.scroll.getCanvas(),
            alert,
            top,
            UIConstants.alertsModalWidth,
        )

        sub = button.onClick.listen(
            lambda _: self.appEvents.ui.modals.alert.send(AlertModalPayload(alert))
        )

        self.alertButtons.append(button)
        self.buttonSubs.append(sub)

        return button

    def destroy(self) -> None:
        super().destroy()

        self.listener.destroy()

        self.title.destroy()

        self.text.destroy()
        for button in self.alertButtons:
            button.destroy()
        for sub in self.buttonSubs:
            sub.cancel()
