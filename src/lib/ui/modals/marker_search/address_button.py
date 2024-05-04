from __future__ import annotations

from panda3d.core import NodePath, PandaNode

from lib.model.location import Location
from lib.ui.context import UIContext
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.components.button import Button, ButtonSkin
from lib.ui.core.components.text import Text
from lib.ui.core.constants import UIConstants
from lib.ui.core.layers import UILayer
from lib.util.events.event_dispatcher import EventDispatcher
from lib.util.events.listener import Listener


class AddressButton(Listener):
    def __init__(
        self,
        ctx: UIContext,
        root: NodePath[PandaNode],
        top: float,
        contentWidth: float,
        location: Location,
    ) -> None:
        super().__init__()

        label = location.getLabel()
        if "\n" in label:
            buttonHeight = UIConstants.addressModalResultButtonHeightDouble
        else:
            buttonHeight = UIConstants.addressModalResultButtonHeight

        self.button = Button(
            root=root,
            ctx=ctx,
            width=contentWidth,
            height=buttonHeight,
            y=-top,
            hAlign=HAlign.LEFT,
            vAlign=VAlign.TOP,
            textSize=UIConstants.fontSizeRegular,
            skin=ButtonSkin.ACCENT,
            bgLayer=UILayer.MODAL_CONTENT_BACKGROUND,
            contentLayer=UILayer.MODAL_CONTENT,
            interactionLayer=UILayer.MODAL_CONTENT_INTERACTION,
        )

        self.labelText = Text(
            root=root,
            font=ctx.fonts.regular,
            text=label,
            x=UIConstants.addressModalResultButtonTextPadding,
            y=-(top + (UIConstants.addressModalResultButtonTextPadding / 2)),
            size=UIConstants.fontSizeRegular,
            vAlign=VAlign.TOP,
            layer=UILayer.MODAL_CONTENT,
        )

        self.onClick = EventDispatcher[Location]()
        self.listen(self.button.onClick, lambda _: self.onClick.send(location))

    def destroy(self) -> None:
        super().destroy()

        self.button.destroy()
        self.labelText.destroy()

        self.onClick.close()
