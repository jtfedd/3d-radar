import webbrowser

from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.ui.context import UIContext
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.components.button import Button, ButtonSkin
from lib.ui.core.components.text import Text
from lib.ui.core.components.text_input import TextInput
from lib.ui.core.constants import UIConstants
from lib.ui.core.layers import UILayer
from lib.ui.messages import maptiler
from lib.util.events.event_dispatcher import EventDispatcher
from lib.util.events.listener import Listener

from ..core.modal import Modal
from ..core.title import ModalTitle


class MapTilerModal(Modal):
    def __init__(
        self,
        ctx: UIContext,
        state: AppState,
        events: AppEvents,
        onContinue: EventDispatcher[None],
    ):
        super().__init__(
            ctx,
            events,
            UIConstants.maptilerModalWidth,
            0,
            closeButton=False,
        )

        self.listener = Listener()
        self.state = state

        self.title = ModalTitle(
            ctx,
            self.topLeft,
            "MapTiler API Key Required",
            UIConstants.maptilerModalWidth,
        )

        top = self.title.height()

        self.description = Text(
            root=self.topLeft,
            font=ctx.fonts.regular,
            text=maptiler.LOCATION_LOOKUPS,
            vAlign=VAlign.TOP,
            y=-(top),
            size=UIConstants.fontSizeRegular,
            layer=UILayer.MODAL_CONTENT,
            hAlign=HAlign.LEFT,
            maxWidth=UIConstants.maptilerModalWidth,
        )

        top += self.description.getHeight() + UIConstants.maptilerModalPadding

        self.mapTilerButton = Button(
            root=self.topLeft,
            ctx=ctx,
            y=-(top),
            width=UIConstants.maptilerModalWidth,
            height=UIConstants.panelInputHeight,
            hAlign=HAlign.LEFT,
            vAlign=VAlign.TOP,
            text="MapTiler",
            bgLayer=UILayer.MODAL_CONTENT_BACKGROUND,
            contentLayer=UILayer.MODAL_CONTENT,
            interactionLayer=UILayer.MODAL_CONTENT_INTERACTION,
            skin=ButtonSkin.ACCENT,
        )
        self.listener.listen(
            self.mapTilerButton.onClick,
            lambda _: webbrowser.open("https://www.maptiler.com/"),
        )

        top += UIConstants.panelInputHeight + UIConstants.maptilerModalPadding

        self.keyInput = TextInput(
            ctx=ctx,
            events=events,
            root=self.topLeft,
            font=ctx.fonts.regular,
            x=UIConstants.maptilerModalWidth
            - (UIConstants.inputPaddingVertical * UIConstants.fontSizeRegular),
            y=-(top),
            hAlign=HAlign.RIGHT,
            vAlign=VAlign.TOP,
            width=UIConstants.maptilerModalWidth * 3 / 4,
            size=UIConstants.fontSizeRegular,
            layer=UILayer.MODAL_CONTENT_INTERACTION,
        )
        self.listener.listen(self.keyInput.onChange, self.handleKeyInput)

        self.keyText = Text(
            root=self.topLeft,
            font=ctx.fonts.regular,
            text="Key:",
            vAlign=VAlign.TOP,
            y=-(top),
            size=UIConstants.fontSizeRegular,
            layer=UILayer.MODAL_CONTENT,
            hAlign=HAlign.LEFT,
        )

        top += UIConstants.panelInputHeight

        self.cancelButton = Button(
            root=self.topLeft,
            ctx=ctx,
            x=UIConstants.maptilerModalWidth / 4,
            y=-(top),
            width=UIConstants.maptilerModalWidth / 3,
            height=UIConstants.modalFooterButtonHeight,
            hAlign=HAlign.CENTER,
            vAlign=VAlign.TOP,
            text="Cancel",
            bgLayer=UILayer.MODAL_CONTENT_BACKGROUND,
            contentLayer=UILayer.MODAL_CONTENT,
            interactionLayer=UILayer.MODAL_CONTENT_INTERACTION,
            skin=ButtonSkin.ACCENT,
        )
        self.listener.listen(self.cancelButton.onClick, lambda _: self.destroy())

        self.continueButton = Button(
            root=self.topLeft,
            ctx=ctx,
            x=UIConstants.maptilerModalWidth * 3 / 4,
            y=-(top),
            width=UIConstants.maptilerModalWidth / 3,
            height=UIConstants.modalFooterButtonHeight,
            hAlign=HAlign.CENTER,
            vAlign=VAlign.TOP,
            text="Continue",
            bgLayer=UILayer.MODAL_CONTENT_BACKGROUND,
            contentLayer=UILayer.MODAL_CONTENT,
            interactionLayer=UILayer.MODAL_CONTENT_INTERACTION,
            skin=ButtonSkin.ACCENT,
            disabled=True,
        )
        self.listener.listen(self.continueButton.onClick, onContinue.send)

        top += UIConstants.modalFooterButtonHeight

        self.updateSize(
            UIConstants.maptilerModalWidth,
            top,
        )

    def handleKeyInput(self, value: str) -> None:
        self.continueButton.setDisabled(value == "")
        self.state.maptilerKey.setValue(value)

    def destroy(self) -> None:
        super().destroy()
        self.listener.destroy()

        self.title.destroy()
        self.description.destroy()
        self.mapTilerButton.destroy()
        self.keyInput.destroy()
        self.keyText.destroy()
        self.cancelButton.destroy()
        self.continueButton.destroy()
