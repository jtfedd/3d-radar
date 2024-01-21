from __future__ import annotations

from typing import List

from panda3d.core import NodePath, PandaNode

from lib.app.events import AppEvents
from lib.model.location import Location
from lib.ui.context import UIContext
from lib.ui.core.constants import UIConstants
from lib.util.events.listener import Listener

from ..address_search.results_component import AddressResultsComponent
from .address_button import AddressButton


class MarkerResult(AddressResultsComponent, Listener):
    def __init__(
        self,
        ctx: UIContext,
        root: NodePath[PandaNode],
        events: AppEvents,
        top: float,
        locations: List[Location],
    ):
        super().__init__()

        self.contentHeight = UIConstants.modalPadding

        buttonListHeight = UIConstants.addressModalResultButtonPadding * (
            len(locations) - 1
        )

        for location in locations:
            if "\n" in location.getLabel():
                buttonListHeight += UIConstants.addressModalResultButtonHeightDouble
            else:
                buttonListHeight += UIConstants.addressModalResultButtonHeight

        (self.scroll, buttonRoot, self.contentHeight, buttonTop) = self.setupButtonRoot(
            ctx, events, top, self.contentHeight, buttonListHeight, root
        )

        self.buttons: List[AddressButton] = []

        for location in locations:
            self.buttons.append(
                AddressButton(
                    ctx,
                    buttonRoot,
                    buttonTop,
                    UIConstants.addressModalWidth,
                    location,
                )
            )

            buttonTop += UIConstants.addressModalResultButtonPadding
            if "\n" in location.getLabel():
                buttonTop += UIConstants.addressModalResultButtonHeightDouble
            else:
                buttonTop += UIConstants.addressModalResultButtonHeight

        for button in self.buttons:
            self.listen(button.onClick, events.ui.modals.markerSelected.send)

    def height(self) -> float:
        return self.contentHeight

    def destroy(self) -> None:
        super().destroy()

        for button in self.buttons:
            button.destroy()

        if self.scroll:
            self.scroll.destroy()
