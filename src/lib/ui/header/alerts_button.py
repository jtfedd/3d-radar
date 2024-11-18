from lib.app.context import AppContext
from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.model.alert_status import AlertStatus
from lib.model.alert_type import AlertType
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.colors import UIColors
from lib.ui.core.components.badge import Badge
from lib.ui.core.components.button import Button
from lib.ui.core.constants import UIConstants
from lib.ui.core.icons import Icons
from lib.util.events.listener import Listener


class AlertsButton(Listener):
    def __init__(self, ctx: AppContext, state: AppState, events: AppEvents) -> None:
        super().__init__()

        self.ctx = ctx
        self.state = state
        self.events = events

        self.root = ctx.anchors.topRight.attachNewNode("alerts-button")
        self.root.setX(-(UIConstants.clockWidth + UIConstants.headerButtonWidth))

        self.badge = Badge(
            root=self.root,
            ctx=ctx,
            x=-UIConstants.headerButtonWidth / 4,
            y=-UIConstants.headerFooterHeight / 4,
            color=UIColors.RED,
            text="",
        )

        self.button = Button(
            root=self.root,
            ctx=ctx,
            width=UIConstants.headerButtonWidth,
            height=UIConstants.headerFooterHeight,
            hAlign=HAlign.RIGHT,
            vAlign=VAlign.TOP,
            icon=Icons.WARNING,
            iconWidth=UIConstants.headerFooterHeight,
            iconHeight=UIConstants.headerFooterHeight,
            disabled=not state.latest.value,
        )

        self.updateBadge()
        self.listen(state.alerts, lambda _: self.updateBadge())
        self.listen(state.latest, lambda latest: self.button.setDisabled(not latest))
        self.listen(self.button.onClick, events.ui.modals.alerts.send)

    def updateBadge(self) -> None:
        alerts = self.state.alerts.value

        if alerts.status == AlertStatus.READY:
            self.badge.hide()
            return

        if alerts.status == AlertStatus.ERROR:
            self.badge.setColor(UIColors.RED)
            self.badge.setText("")
            return

        if (
            AlertType.TORNADO_WARNING in alerts.alerts
            and len(alerts.alerts[AlertType.TORNADO_WARNING]) > 0
        ):
            self.badge.setColor(UIColors.RED)
        else:
            self.badge.setColor(UIColors.ORANGE)

        count = alerts.count()

        if count > 0:
            self.badge.setText(str(count))
            self.badge.show()
        else:
            self.badge.hide()

    def destroy(self) -> None:
        super().destroy()

        self.button.destroy()
        self.badge.destroy()
