from __future__ import annotations

from panda3d.core import NodePath, PandaNode

from lib.app.context import AppContext
from lib.model.radar_station import RadarStation
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.components.button import Button, ButtonSkin
from lib.ui.core.components.text import Text
from lib.ui.core.constants import UIConstants
from lib.ui.core.layers import UILayer
from lib.util.events.event_dispatcher import EventDispatcher
from lib.util.events.listener import Listener


class RadarButton(Listener):
    def __init__(
        self,
        ctx: AppContext,
        root: NodePath[PandaNode],
        top: float,
        contentWidth: float,
        radarStation: RadarStation,
        distance: float,
    ) -> None:
        super().__init__()

        self.button = Button(
            root=root,
            ctx=ctx,
            width=contentWidth,
            height=UIConstants.addressModalResultButtonHeight,
            y=-top,
            hAlign=HAlign.LEFT,
            vAlign=VAlign.TOP,
            bgLayer=UILayer.MODAL_CONTENT_BACKGROUND,
            contentLayer=UILayer.MODAL_CONTENT,
            interactionLayer=UILayer.MODAL_CONTENT_INTERACTION,
            textSize=UIConstants.fontSizeRegular,
            skin=ButtonSkin.ACCENT,
        )

        self.nameText = Text(
            root=root,
            font=ctx.fonts.regular,
            text=radarStation.stationID + ": " + radarStation.name,
            x=UIConstants.addressModalResultButtonTextPadding,
            y=-(top + UIConstants.addressModalResultButtonHeight / 2),
            size=UIConstants.fontSizeRegular,
            vAlign=VAlign.CENTER,
            layer=UILayer.MODAL_CONTENT,
        )

        self.distText = Text(
            root=root,
            font=ctx.fonts.regular,
            text=f"{distance:.1f} km",
            x=contentWidth - UIConstants.addressModalResultButtonTextPadding,
            y=-(top + UIConstants.addressModalResultButtonHeight / 2),
            size=UIConstants.fontSizeRegular,
            vAlign=VAlign.CENTER,
            hAlign=HAlign.RIGHT,
            layer=UILayer.MODAL_CONTENT,
        )

        self.onClick = EventDispatcher[str]()
        self.listen(
            self.button.onClick, lambda _: self.onClick.send(radarStation.stationID)
        )

    def destroy(self) -> None:
        super().destroy()

        self.button.destroy()

        self.nameText.destroy()
        self.distText.destroy()

        self.onClick.close()
