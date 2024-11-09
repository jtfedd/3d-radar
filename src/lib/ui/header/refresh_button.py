import math

from direct.task.Task import Task

from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.ui.context import UIContext
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.colors import UIColors
from lib.ui.core.components.button import Button
from lib.ui.core.components.image import Image
from lib.ui.core.constants import UIConstants
from lib.ui.core.icons import Icons
from lib.ui.core.layers import UILayer
from lib.util.events.listener import Listener


class RefreshButton(Listener):
    def __init__(self, ctx: UIContext, state: AppState, events: AppEvents) -> None:
        super().__init__()

        self.root = ctx.anchors.topRight.attachNewNode("refresh-button")
        self.root.setX(-UIConstants.clockWidth)

        self.loadingStart = 0.0

        self.button = Button(
            root=self.root,
            ctx=ctx,
            width=UIConstants.headerButtonWidth,
            height=UIConstants.headerFooterHeight,
            hAlign=HAlign.RIGHT,
            vAlign=VAlign.TOP,
            disabled=not state.latest.value,
        )

        self.refreshIcon = Image(
            root=self.root,
            image=Icons.REFRESH,
            color=UIColors.CONTENT,
            layer=UILayer.CONTENT,
            x=-UIConstants.headerButtonWidth / 2,
            vAlign=VAlign.TOP,
            width=UIConstants.headerFooterHeight,
            height=UIConstants.headerFooterHeight,
        )

        self.loadingIcon = Image(
            root=self.root,
            image=Icons.LOADING,
            color=UIColors.CONTENT,
            layer=UILayer.CONTENT,
            x=-UIConstants.headerButtonWidth / 2,
            vAlign=VAlign.TOP,
            width=UIConstants.headerFooterHeight,
            height=UIConstants.headerFooterHeight,
        )

        self.bind(state.latest, lambda latest: self.button.setDisabled(not latest))
        self.bind(
            state.latest,
            lambda latest: self.refreshIcon.updateColor(
                UIColors.CONTENT if latest else UIColors.CONTENT_DISABLED
            ),
        )
        self.bind(
            state.latest,
            lambda latest: self.loadingIcon.updateColor(
                UIColors.CONTENT if latest else UIColors.CONTENT_DISABLED
            ),
        )
        self.listen(self.button.onClick, events.refreshData.send)
        self.bind(state.loadingData, self.updateLoading)

        self.spinnerTask = ctx.appContext.base.taskMgr.add(self.updateSpinner, "spin")

    def updateLoading(self, loading: bool) -> None:
        if loading:
            self.loadingStart = self.spinnerTask.time
            self.loadingIcon.show()
            self.refreshIcon.hide()
        else:
            self.refreshIcon.show()
            self.loadingIcon.hide()

    def updateSpinner(self, task: Task) -> int:
        loadingTime = task.time - self.loadingStart
        spinnerAngle = math.floor(loadingTime * 6) * 45
        self.loadingIcon.card.setR(spinnerAngle)

        return task.cont

    def destroy(self) -> None:
        super().destroy()

        self.spinnerTask.cancel()

        self.refreshIcon.destroy()
        self.button.destroy()
        self.root.removeNode()
