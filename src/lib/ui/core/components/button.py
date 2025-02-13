from __future__ import annotations

from typing import Callable

import direct.gui.DirectGuiGlobals as DGG
from direct.gui.DirectButton import DirectButton
from direct.task.Task import Task
from panda3d.core import DynamicTextFont, NodePath, PandaNode, TransparencyAttrib, Vec4

from lib.app.context import AppContext
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.colors import UIColors
from lib.ui.core.components.background_card import BackgroundCard
from lib.ui.core.components.image import Image
from lib.ui.core.components.text import Text
from lib.ui.core.constants import UIConstants
from lib.ui.core.layers import UILayer
from lib.ui.core.util import correctXForAlignment, correctYForAlignment
from lib.util.events.event_dispatcher import EventDispatcher

from .component import Component


class ButtonSkin:
    INSET: ButtonSkin
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


ButtonSkin.INSET = ButtonSkin(
    ready=UIColors.INSET,
    hover=UIColors.HOVER,
    depressed=UIColors.INSET,
    disabled=UIColors.BACKGROUND_DISABLED,
    content=UIColors.CONTENT,
    contentDisabled=UIColors.CONTENT_DISABLED,
)

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


class Button(Component):
    def __init__(
        self,
        root: NodePath[PandaNode],
        ctx: AppContext,
        width: float,
        height: float,
        x: float = 0,
        y: float = 0,
        hAlign: HAlign = HAlign.CENTER,
        vAlign: VAlign = VAlign.CENTER,
        bgLayer: UILayer = UILayer.CONTENT_BACKGROUND,
        contentLayer: UILayer = UILayer.CONTENT,
        interactionLayer: UILayer = UILayer.CONTENT_INTERACTION,
        toggleState: bool = False,
        text: str | None = None,
        font: DynamicTextFont | None = None,
        textSize: float = UIConstants.fontSizeRegular,
        icon: str | None = None,
        toggleIcon: str | None = None,
        iconWidth: float = 0.0,
        iconHeight: float = 0.0,
        skin: ButtonSkin = ButtonSkin.DARK,
        toggleSkin: ButtonSkin = ButtonSkin.LIGHT,
        disabled: bool = False,
    ) -> None:
        self.toggleState = toggleState
        self.disabled = disabled

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
            layer=bgLayer,
        )

        self.imageContentFactory: Callable[[str], Image] = lambda i: Image(
            root=root,
            image=i,
            width=iconWidth,
            height=iconHeight,
            x=xPos,
            y=yPos,
            hAlign=HAlign.CENTER,
            vAlign=VAlign.CENTER,
            layer=contentLayer,
        )

        self.textContentFactory: Callable[[str], Text] = lambda t: Text(
            root=root,
            font=font or ctx.fonts.medium,
            text=t,
            x=xPos,
            y=yPos,
            hAlign=HAlign.CENTER,
            vAlign=VAlign.CENTER,
            size=textSize,
            layer=contentLayer,
        )

        self.content: Text | Image | None = None
        if icon:
            self.content = self.imageContentFactory(icon)
        elif text:
            self.content = self.textContentFactory(text)

        self.toggleIcon: Image | None = None
        if toggleIcon:
            self.toggleIcon = self.imageContentFactory(toggleIcon)

        self.button = DirectButton(
            parent=root,
            command=self.handleClick,
            pos=(xPos, 0, yPos),
            frameSize=(-width / 2, width / 2, -height / 2, height / 2),
            borderWidth=(0, 0),
            frameColor=UIColors.TRANSPARENT,
            rolloverSound=None,
            clickSound=None,
            state=self.getState(),
        )

        self.button.setBin("fixed", interactionLayer.value)
        self.button.setTransparency(TransparencyAttrib.MAlpha)
        self.button.setAlphaScale(0)

        self.update()

        self.onClick = EventDispatcher[None]()

        self.updateTask = ctx.base.addTask(lambda _: self.update(), "button-update")

    def getState(self) -> str:
        if self.disabled:
            return DGG.DISABLED
        return DGG.NORMAL

    def update(self) -> int:
        buttonState = self.button.guiItem.getState()  # type: ignore

        # Toggled state should override ready and hover
        if self.toggleState:
            if self.toggleIcon:
                self.toggleIcon.show()
                if self.content:
                    self.content.hide()

                self.toggleIcon.updateColor(
                    self.toggleSkin.getContentColor(buttonState)
                )

            self.background.updateColor(self.toggleSkin.getBackgroundColor(buttonState))

            if self.content:
                self.content.updateColor(self.toggleSkin.getContentColor(buttonState))
        else:
            if self.toggleIcon:
                self.toggleIcon.hide()
                if self.content:
                    self.content.show()

            self.background.updateColor(self.skin.getBackgroundColor(buttonState))

            if self.content:
                self.content.updateColor(self.skin.getContentColor(buttonState))

        return Task.cont

    def setIcon(self, icon: str) -> None:
        if self.content:
            self.content.destroy()
        self.content = self.imageContentFactory(icon)

    def handleClick(self) -> None:
        self.onClick.send(None)

    def setToggleState(self, toggleState: bool) -> None:
        self.toggleState = toggleState

    def setDisabled(self, disabled: bool) -> None:
        self.disabled = disabled
        self.button["state"] = self.getState()

    def destroy(self) -> None:
        self.updateTask.cancel()
        self.button.destroy()
        self.background.destroy()
        self.onClick.close()

        if self.content:
            self.content.destroy()
        if self.toggleIcon:
            self.toggleIcon.destroy()
