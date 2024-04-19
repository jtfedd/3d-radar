from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.model.alert_status import AlertStatus
from lib.model.alert_type import AlertType
from lib.ui.context import UIContext
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.colors import UIColors
from lib.ui.core.components.badge import Badge
from lib.ui.core.components.button import Button
from lib.ui.core.constants import UIConstants
from lib.ui.core.icons import Icons
from lib.util.events.listener import Listener


class AlertsButton(Listener):
    def __init__(self, ctx: UIContext, state: AppState, events: AppEvents) -> None:
        super().__init__()

        self.ctx = ctx
        self.state = state
        self.events = events

        self.badge = Badge(
            root=ctx.anchors.topRight,
            ctx=ctx,
            x=-(UIConstants.clockWidth + UIConstants.headerButtonWidth / 4),
            y=-UIConstants.headerFooterHeight / 4,
            color=UIColors.RED,
            text="",
        )

        self.button = Button(
            root=ctx.anchors.topRight,
            ctx=ctx,
            width=UIConstants.headerButtonWidth,
            height=UIConstants.headerFooterHeight,
            x=-UIConstants.clockWidth,
            hAlign=HAlign.RIGHT,
            vAlign=VAlign.TOP,
            icon=Icons.WARNING,
            iconWidth=UIConstants.headerFooterHeight,
            iconHeight=UIConstants.headerFooterHeight,
            disabled=not state.latest,
        )

        self.updateBadge()
        self.listen(state.alerts, lambda _: self.updateBadge())
        self.listen(state.latest, lambda latest: self.button.setDisabled(not latest))

    def updateBadge(self) -> None:
        alerts = self.state.alerts.value

        if alerts.status != AlertStatus.LOADED:
            self.badge.hide()

        if AlertType.TORNADO_WARNING in alerts.alerts:
            self.badge.setColor(UIColors.RED)
        else:
            self.badge.setColor(UIColors.ORANGE)

        count = 0

        if AlertType.TORNADO_WARNING in alerts.alerts:
            count += len(alerts.alerts[AlertType.TORNADO_WARNING])

        if AlertType.SEVERE_THUNDERSTORM_WARNING in alerts.alerts:
            count += len(alerts.alerts[AlertType.SEVERE_THUNDERSTORM_WARNING])

        if count > 0:
            self.badge.setText(str(count))
            self.badge.show()
        else:
            self.badge.hide()

    def destroy(self) -> None:
        super().destroy()

        self.button.destroy()
        self.badge.destroy()
