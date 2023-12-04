from __future__ import annotations

import direct.gui.DirectGuiGlobals as DGG
from direct.gui.DirectButton import DirectButton
from direct.task.Task import Task
from panda3d.core import NodePath, PandaNode, TransparencyAttrib, Vec4

from lib.ui.context import UIContext
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.colors import UIColors
from lib.ui.core.components.background_card import BackgroundCard
from lib.ui.core.components.image import Image
from lib.ui.core.components.text import Text
from lib.ui.core.constants import UIConstants
from lib.ui.core.layers import UILayer
from lib.ui.core.util import correctXForAlignment, correctYForAlignment
from lib.util.events.event_dispatcher import EventDispatcher


class ButtonSkin:
    DARK: ButtonSkin
    ACCENT: ButtonSkin
    LIGHT: ButtonSkin

    def __init__(
        self,
        ready: Vec4,
        hover: Vec4,
        depressed: Vec4,
        disabled: Vec4,
        content: Vec4,
        contentDisabled: Vec4,
    ):
        self.ready = ready
        self.hover = hover
        self.depressed = depressed
        self.disabled = disabled

        self.content = content
        self.contentDisabled = contentDisabled

    def getBackgroundColor(self, buttonState: int) -> Vec4:
        if buttonState == DGG.BUTTON_READY_STATE:
            return self.ready
        if buttonState == DGG.BUTTON_ROLLOVER_STATE:
            return self.hover
        if buttonState == DGG.BUTTON_DEPRESSED_STATE:
            return self.depressed

        return self.disabled

    def getContentColor(self, buttonState: int) -> Vec4:
        if buttonState == DGG.BUTTON_INACTIVE_STATE:
            return self.contentDisabled

        return self.content


ButtonSkin.DARK = ButtonSkin(
    ready=UIColors.BACKGROUND,
    hover=UIColors.HOVER,
    depressed=UIColors.DEPRESSED,
    disabled=UIColors.BACKGROUND_DISABLED,
    content=UIColors.CONTENT,
    contentDisabled=UIColors.CONTENT_DISABLED,
)

ButtonSkin.ACCENT = ButtonSkin(
    ready=UIColors.ACCENT,
    hover=UIColors.ACCENT_HOVER,
    depressed=UIColors.DEPRESSED,
    disabled=UIColors.BACKGROUND_DISABLED_ACCENT,
    content=UIColors.CONTENT,
    contentDisabled=UIColors.CONTENT_DISABLED,
)

ButtonSkin.LIGHT = ButtonSkin(
    ready=UIColors.BACKGROUND_LIGHT,
    hover=UIColors.HOVER_LIGHT,
    depressed=UIColors.DEPRESSED_LIGHT,
    disabled=UIColors.BACKGROUND_DISABLED_LIGHT,
    content=UIColors.CONTENT_LIGHT,
    contentDisabled=UIColors.CONTENT_DISABLED_LIGHT,
)


class Button:
    def __init__(
        self,
        root: NodePath[PandaNode],
        ctx: UIContext,
        width: float,
        height: float,
        x: float = 0,
        y: float = 0,
        hAlign: HAlign = HAlign.CENTER,
        vAlign: VAlign = VAlign.CENTER,
        layer: UILayer = UILayer.INTERACTION,
        toggleState: bool = False,
        text: str | None = None,
        textSize: float = UIConstants.fontSizeRegular,
        icon: str | None = None,
        iconWidth: float = 0.0,
        iconHeight: float = 0.0,
        skin: ButtonSkin = ButtonSkin.DARK,
        toggleSkin: ButtonSkin = ButtonSkin.LIGHT,
    ) -> None:
        self.toggleState = toggleState

        xPos = correctXForAlignment(x, width, hAlign)
        yPos = correctYForAlignment(y, height, vAlign)

        self.skin = skin
        self.toggleSkin = toggleSkin

        self.background = BackgroundCard(
            root=root,
            width=width,
            height=height,
            x=x,
            y=y,
            hAlign=hAlign,
            vAlign=vAlign,
            layer=UILayer(layer.value - 2),
        )

        self.content: Text | Image

        if icon:
            self.content = Image(
                root=root,
                image=icon,
                width=iconWidth,
                height=iconHeight,
                x=xPos,
                y=yPos,
                hAlign=HAlign.CENTER,
                vAlign=VAlign.CENTER,
                layer=UILayer(layer.value - 1),
            )
        elif text:
            self.content = Text(
                root=root,
                font=ctx.fonts.medium,
                text=text,
                x=xPos,
                y=yPos,
                hAlign=HAlign.CENTER,
                vAlign=VAlign.CENTER,
                size=textSize,
                layer=UILayer(layer.value - 1),
            )

        self.button = DirectButton(
            parent=root,
            image="assets/white.png",
            command=self.handleClick,
            pos=(xPos, 0, yPos),
            scale=(width / 2, 1, height / 2),
            borderWidth=(0, 0),
            frameColor=UIColors.TRANSPARENT,
            rolloverSound=None,
            clickSound=None,
        )

        self.button.setBin("fixed", layer.value)
        self.button.setTransparency(TransparencyAttrib.MAlpha)
        self.button.setAlphaScale(0)

        self.update()

        self.onClick = EventDispatcher[None]()

        self.updateTask = ctx.appContext.base.addTask(
            lambda _: self.update(), "button-update"
        )

    def update(self) -> int:
        buttonState = self.button.guiItem.getState()  # type: ignore

        # Toggled state should override ready and hover
        if self.toggleState:
            self.background.updateColor(self.toggleSkin.getBackgroundColor(buttonState))
            self.content.updateColor(self.toggleSkin.getContentColor(buttonState))
        else:
            self.background.updateColor(self.skin.getBackgroundColor(buttonState))
            self.content.updateColor(self.skin.getContentColor(buttonState))

        return Task.cont

    def handleClick(self) -> None:
        self.onClick.send(None)

    def setToggleState(self, toggleState: bool) -> None:
        self.toggleState = toggleState

    def destroy(self) -> None:
        self.updateTask.cancel()
        self.button.destroy()
        self.background.destroy()
        self.content.destroy()
        self.onClick.close()
