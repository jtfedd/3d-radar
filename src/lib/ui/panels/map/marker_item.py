from __future__ import annotations

from panda3d.core import NodePath, PandaNode

from lib.app.events import AppEvents
from lib.model.location_marker import LocationMarker
from lib.ui.context import UIContext
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.colors import UIColors
from lib.ui.core.components.background_card import BackgroundCard
from lib.ui.core.components.button import Button, ButtonSkin
from lib.ui.core.components.text import Text
from lib.ui.core.constants import UIConstants
from lib.ui.core.icons import Icons
from lib.ui.core.layers import UILayer
from lib.util.events.listener import Listener


class MarkerItem(Listener):
    def __init__(
        self,
        root: NodePath[PandaNode],
        ctx: UIContext,
        events: AppEvents,
        item: LocationMarker,
        top: float,
    ) -> None:
        super().__init__()

        self.root = root.attachNewNode("marker-item")
        self.root.setZ(-top)
        self.root.setX(UIConstants.panelPadding)

        self.text = Text(
            self.root,
            ctx.fonts.regular,
            item.location.getLabel(alwaysBreak=True),
            x=UIConstants.markerItemTextLeft,
            y=-UIConstants.markerItemPadding,
            vAlign=VAlign.TOP,
            maxWidth=UIConstants.markerItemTextWidth,
        )

        self.contentHeight = max(
            UIConstants.markerItemMinHeight,
            self.text.getHeight() + (2 * UIConstants.markerItemPadding),
        )

        self.background = BackgroundCard(
            self.root,
            width=UIConstants.panelContentWidth,
            height=self.contentHeight,
            color=UIColors.ACCENT,
            hAlign=HAlign.LEFT,
            vAlign=VAlign.TOP,
            layer=UILayer.BACKGROUND_DECORATION,
        )

        self.visibilityButton = Button(
            root=self.root,
            ctx=ctx,
            width=UIConstants.markerItemButtonSize,
            height=UIConstants.markerItemButtonSize,
            x=UIConstants.markerItemPadding,
            y=-(self.contentHeight / 2),
            hAlign=HAlign.LEFT,
            vAlign=VAlign.CENTER,
            toggleState=item.visible,
            icon=Icons.INVISIBLE,
            toggleIcon=Icons.VISIBLE,
            iconWidth=UIConstants.markerItemButtonSize,
            iconHeight=UIConstants.markerItemButtonSize,
            skin=ButtonSkin.ACCENT,
            toggleSkin=ButtonSkin.ACCENT,
        )

        self.trashButton = Button(
            root=self.root,
            ctx=ctx,
            width=UIConstants.markerItemButtonSize,
            height=UIConstants.markerItemButtonSize,
            x=UIConstants.panelContentWidth - UIConstants.markerItemPadding,
            y=-(self.contentHeight / 2),
            hAlign=HAlign.RIGHT,
            vAlign=VAlign.CENTER,
            icon=Icons.TRASH,
            iconWidth=UIConstants.markerItemButtonSize,
            iconHeight=UIConstants.markerItemButtonSize,
            skin=ButtonSkin.ACCENT,
        )

        self.listen(
            self.visibilityButton.onClick,
            lambda _: events.ui.panels.toggleMarker.send(item.id),
        )

        self.listen(
            self.trashButton.onClick,
            lambda _: events.ui.panels.removeMarker.send(item.id),
        )

    def height(self) -> float:
        return self.contentHeight

    def destroy(self) -> None:
        super().destroy()

        self.text.destroy()
        self.background.destroy()
        self.visibilityButton.destroy()
        self.trashButton.destroy()

        self.root.removeNode()
