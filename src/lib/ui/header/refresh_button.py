from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.ui.context import UIContext
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.components.button import Button
from lib.ui.core.constants import UIConstants
from lib.ui.core.icons import Icons
from lib.util.events.listener import Listener


class RefreshButton(Listener):
    def __init__(self, ctx: UIContext, state: AppState, events: AppEvents) -> None:
        super().__init__()

        self.button = Button(
            root=ctx.anchors.topRight,
            ctx=ctx,
            width=UIConstants.headerButtonWidth,
            height=UIConstants.headerFooterHeight,
            x=-UIConstants.clockWidth,
            hAlign=HAlign.RIGHT,
            vAlign=VAlign.TOP,
            icon=Icons.REFRESH,
            iconWidth=UIConstants.headerFooterHeight,
            iconHeight=UIConstants.headerFooterHeight,
            disabled=not state.latest.value,
        )

        self.listen(state.latest, lambda latest: self.button.setDisabled(not latest))
        self.listen(self.button.onClick, events.refreshData.send)
        self.bind(state.loadingData, self.updateIcon)

    def updateIcon(self, loading: bool) -> None:
        if loading:
            self.button.setIcon(Icons.LOADING)
        else:
            self.button.setIcon(Icons.REFRESH)

    def destroy(self) -> None:
        super().destroy()

        self.button.destroy()
