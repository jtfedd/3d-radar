from __future__ import annotations

from panda3d.core import NodePath, PandaNode

from lib.app.events import AppEvents
from lib.model.location import Location
from lib.ui.context import UIContext
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.components.button import Button, ButtonSkin
from lib.ui.core.constants import UIConstants
from lib.ui.core.layers import UILayer
from lib.util.events.listener import Listener
from lib.util.optional import unwrap

from ..address_search.results_component import AddressResultsComponent
from ..core.text import ModalText


class TimezoneResult(AddressResultsComponent, Listener):
    def __init__(
        self,
        ctx: UIContext,
        root: NodePath[PandaNode],
        events: AppEvents,
        top: float,
        location: Location,
        tz: str | None,
    ):
        super().__init__()

        self.contentHeight = 0.0

        text = location.getLabel()
        if len(text) > 30:
            text = location.getLabel2()

        self.locationText = ModalText(ctx, root, top, text)
        self.contentHeight = self.locationText.height() + UIConstants.modalPadding

        self.result: Button | ModalText

        if tz:
            self.result = Button(
                root=root,
                ctx=ctx,
                width=UIConstants.addressModalWidth,
                height=0.05,
                y=-(top + self.contentHeight),
                hAlign=HAlign.LEFT,
                vAlign=VAlign.TOP,
                layer=UILayer.MODAL_CONTENT_INTERACTION,
                textSize=UIConstants.fontSizeRegular,
                text=tz,
                skin=ButtonSkin.ACCENT,
            )

            self.contentHeight += 0.05

            self.listen(
                self.result.onClick,
                lambda _: events.ui.modals.timeZoneSelected.send(unwrap(tz)),
            )
        else:
            self.result = ModalText(ctx, root, top, "No timezone found.")

    def height(self) -> float:
        return self.contentHeight

    def destroy(self) -> None:
        super().destroy()

        self.locationText.destroy()
        self.result.destroy()
