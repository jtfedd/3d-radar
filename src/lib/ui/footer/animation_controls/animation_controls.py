import datetime

from lib.app.context import AppContext
from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.colors import UIColors
from lib.ui.core.components.background_card import BackgroundCard
from lib.ui.core.components.button import Button, ButtonSkin
from lib.ui.core.components.slider import Slider
from lib.ui.core.components.text import Text
from lib.ui.core.constants import UIConstants
from lib.ui.core.icons import Icons
from lib.ui.core.layers import UILayer
from lib.util.events.listener import Listener


class AnimationControls(Listener):
    def __init__(self, ctx: AppContext, state: AppState, events: AppEvents) -> None:
        super().__init__()

        self.ctx = ctx
        self.state = state

        self.background = BackgroundCard(
            ctx.anchors.bottom,
            width=UIConstants.animationControlsWidth,
            height=UIConstants.headerFooterHeight,
            color=UIColors.INSET,
            vAlign=VAlign.BOTTOM,
            layer=UILayer.BACKGROUND_DECORATION,
        )

        self.sliderBackground = BackgroundCard(
            ctx.anchors.bottom,
            width=UIConstants.animationSliderWidth
            + (2 * UIConstants.animationSliderPadding),
            height=UIConstants.headerFooterHeight,
            color=UIColors.BLACK,
            vAlign=VAlign.BOTTOM,
            layer=UILayer.CONTENT_BACKGROUND,
        )

        self.select2D = Button(
            ctx.anchors.bottom,
            ctx,
            UIConstants.animationButtonWidth,
            UIConstants.headerFooterHeight / 2,
            -UIConstants.animationControlsWidth / 2,
            UIConstants.headerFooterHeight / 2,
            hAlign=HAlign.LEFT,
            vAlign=VAlign.BOTTOM,
            text="2D",
            skin=ButtonSkin.INSET,
            toggleSkin=ButtonSkin.LIGHT,
            toggleState=(not state.view3D.getValue()),
        )

        self.select3D = Button(
            ctx.anchors.bottom,
            ctx,
            UIConstants.animationButtonWidth,
            UIConstants.headerFooterHeight / 2,
            -UIConstants.animationControlsWidth / 2,
            0,
            hAlign=HAlign.LEFT,
            vAlign=VAlign.BOTTOM,
            text="3D",
            skin=ButtonSkin.INSET,
            toggleSkin=ButtonSkin.LIGHT,
            toggleState=state.view3D.getValue(),
        )

        self.play = Button(
            ctx.anchors.bottom,
            ctx,
            UIConstants.animationButtonWidth,
            UIConstants.headerFooterHeight,
            -UIConstants.animationControlsWidth / 2
            + (2 * UIConstants.animationButtonWidth),
            0,
            hAlign=HAlign.LEFT,
            vAlign=VAlign.BOTTOM,
            icon=Icons.PLAY,
            iconHeight=UIConstants.headerFooterHeight,
            iconWidth=UIConstants.headerFooterHeight,
            skin=ButtonSkin.INSET,
        )

        self.previous = Button(
            ctx.anchors.bottom,
            ctx,
            UIConstants.animationButtonWidth,
            UIConstants.headerFooterHeight,
            -UIConstants.animationControlsWidth / 2
            + (1 * UIConstants.animationButtonWidth),
            0,
            hAlign=HAlign.LEFT,
            vAlign=VAlign.BOTTOM,
            icon=Icons.ARROWS,
            iconHeight=UIConstants.headerFooterHeight,
            iconWidth=-UIConstants.headerFooterHeight,
            skin=ButtonSkin.INSET,
        )

        self.next = Button(
            ctx.anchors.bottom,
            ctx,
            UIConstants.animationButtonWidth,
            UIConstants.headerFooterHeight,
            -UIConstants.animationControlsWidth / 2
            + (3 * UIConstants.animationButtonWidth),
            0,
            hAlign=HAlign.LEFT,
            vAlign=VAlign.BOTTOM,
            icon=Icons.ARROWS,
            iconHeight=UIConstants.headerFooterHeight,
            iconWidth=UIConstants.headerFooterHeight,
            skin=ButtonSkin.INSET,
        )

        self.animationSlider = Slider(
            ctx.anchors.bottom,
            0,
            UIConstants.headerFooterHeight / 2,
            UIConstants.animationSliderWidth,
            hAlign=HAlign.CENTER,
            initialValue=1.0,
            valueRange=(0, 1),
        )

        self.time = Text(
            ctx.anchors.bottom,
            ctx.fonts.mono,
            self.getClockStr(),
            x=UIConstants.animationControlsWidth / 2
            - UIConstants.animationButtonGroupWidth / 2,
            y=UIConstants.headerFooterHeight / 2,
            hAlign=HAlign.CENTER,
            vAlign=VAlign.BOTTOM,
        )

        self.listen(
            state.animationTime, lambda _: self.time.updateText(self.getClockStr())
        )

        self.listen(self.play.onClick, events.animation.play.send)
        self.listen(self.next.onClick, events.animation.next.send)
        self.listen(self.previous.onClick, events.animation.previous.send)
        self.bind(state.animationPlaying, self.updatePlayButton)

        self.listen(self.animationSlider.onValueChange, self.handleSliderChange)
        self.listen(state.animationTime, self.handleAnimationUpdate)

        self.listen(self.select2D.onClick, lambda _: state.view3D.setValue(False))
        self.listen(self.select3D.onClick, lambda _: state.view3D.setValue(True))
        self.listen(state.view3D, lambda value: self.select2D.setToggleState(not value))
        self.listen(state.view3D, self.select3D.setToggleState)

    def handleSliderChange(self, value: float) -> None:
        animationStart, animationEnd = self.state.animationBounds.value
        animationTime = animationStart + value * (animationEnd - animationStart)

        # To avoid programmatic updates causing the slider to think it moved, only
        # send events when the value difference is greater than 1 tenth of a second
        if abs(animationTime - self.state.animationTime.getValue()) > 0.1:
            self.state.animationTime.setValue(animationTime)
            self.state.animationPlaying.setValue(False)

    def handleAnimationUpdate(self, value: float) -> None:
        animationStart, animationEnd = self.state.animationBounds.value
        normalizedValue = (value - animationStart) / (animationEnd - animationStart)
        normalizedValue = max(0, min(1, normalizedValue))
        self.animationSlider.setValue(normalizedValue)

    def updatePlayButton(self, playing: bool) -> None:
        if playing:
            self.play.setIcon(Icons.PAUSE)
        else:
            self.play.setIcon(Icons.PLAY)

    def getClockStr(self) -> str:
        return self.ctx.timeUtil.formatTime(
            datetime.datetime.fromtimestamp(
                self.state.animationTime.value, tz=datetime.timezone.utc
            ),
            sep="\n",
            seconds=True,
        )

    def destroy(self) -> None:
        super().destroy()

        self.background.destroy()
        self.sliderBackground.destroy()
        self.select2D.destroy()
        self.select3D.destroy()
        self.play.destroy()
        self.previous.destroy()
        self.next.destroy()
        self.animationSlider.destroy()
        self.time.destroy()
