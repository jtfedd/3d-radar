from lib.app.context import AppContext
from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.colors import UIColors
from lib.ui.core.components.background_card import BackgroundCard
from lib.ui.core.components.button import Button, ButtonSkin
from lib.ui.core.components.slider import Slider
from lib.ui.core.constants import UIConstants
from lib.ui.core.icons import Icons
from lib.ui.core.layers import UILayer
from lib.util.events.listener import Listener


class AnimationControls(Listener):
    def __init__(self, ctx: AppContext, state: AppState, events: AppEvents) -> None:
        super().__init__()

        self.ctx = ctx

        self.background = BackgroundCard(
            ctx.anchors.bottom,
            width=UIConstants.animationControlsWidth,
            height=UIConstants.headerFooterHeight,
            color=UIColors.INSET,
            vAlign=VAlign.BOTTOM,
            layer=UILayer.BACKGROUND_DECORATION,
        )

        self.play = Button(
            ctx.anchors.bottom,
            ctx,
            UIConstants.animationButtonWidth,
            UIConstants.headerFooterHeight,
            -UIConstants.animationControlsWidth / 2 + UIConstants.animationButtonWidth,
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
            -UIConstants.animationControlsWidth / 2,
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
            + 2 * UIConstants.animationButtonWidth,
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

        self.listen(self.play.onClick, events.animation.play.send)
        self.listen(self.next.onClick, events.animation.next.send)
        self.listen(self.previous.onClick, events.animation.previous.send)
        self.listen(self.animationSlider.onValueChange, events.animation.slider.send)
        self.listen(events.animation.animationProgress, self.animationSlider.setValue)

        self.updatePlayButton(state.animationPlaying.value)
        self.listen(state.animationPlaying, self.updatePlayButton)

    def updatePlayButton(self, playing: bool) -> None:
        if playing:
            self.play.setIcon(Icons.PAUSE)
        else:
            self.play.setIcon(Icons.PLAY)

    def destroy(self) -> None:
        super().destroy()

        self.background.destroy()
        self.play.destroy()
        self.previous.destroy()
        self.next.destroy()
