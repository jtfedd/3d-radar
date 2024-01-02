from abc import ABC, abstractmethod
from typing import List

from lib.app.events import AppEvents
from lib.model.location import Location
from lib.ui.context import UIContext
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.components.button import Button, ButtonSkin
from lib.ui.core.components.text_input import TextInput
from lib.ui.core.constants import UIConstants
from lib.ui.core.layers import UILayer
from lib.util.events.listener import Listener

from ..core.modal import Modal
from ..core.text import ModalText
from ..core.title import ModalTitle
from .error_result_component import ErrorResultComponent
from .results_component import AddressResultsComponent


class AddressSearchModal(Modal, ABC):
    def __init__(self, ctx: UIContext, events: AppEvents, title: str, description: str):
        super().__init__(ctx, events, UIConstants.addressModalWidth, 0)

        self.listener = Listener()

        self.ctx = ctx

        top = 0.0

        self.title = ModalTitle(
            ctx,
            self.topLeft,
            title,
            modalContentWidth=UIConstants.addressModalWidth,
        )
        top += self.title.height()

        self.detailText = ModalText(
            ctx,
            self.topLeft,
            top,
            description,
        )
        top += self.detailText.height()
        top += UIConstants.modalPadding

        self.searchbar = TextInput(
            ctx,
            events,
            self.topLeft,
            font=ctx.fonts.regular,
            size=UIConstants.fontSizeRegular,
            width=UIConstants.addressModalWidth,
            y=-top,
            hAlign=HAlign.LEFT,
            vAlign=VAlign.TOP,
            layer=UILayer.MODAL_CONTENT_INTERACTION,
        )
        top += UIConstants.addressModalSearchbarHeight

        self.searchbar.onCommit.listen(self.search)

        self.cancelButton = Button(
            root=self.bottomLeft,
            ctx=ctx,
            width=UIConstants.modalFooterButtonWidth,
            height=UIConstants.modalFooterButtonHeight,
            x=UIConstants.addressModalWidth / 2,
            hAlign=HAlign.CENTER,
            vAlign=VAlign.BOTTOM,
            layer=UILayer.MODAL_CONTENT_INTERACTION,
            textSize=UIConstants.fontSizeRegular,
            skin=ButtonSkin.ACCENT,
            text="Cancel",
        )

        self.headerHeight = top
        self.footerHeight = (
            UIConstants.modalFooterButtonHeight + UIConstants.modalPadding
        )

        self.resultsComponent: AddressResultsComponent | None = None

        self.updateSize(
            UIConstants.addressModalWidth, self.headerHeight + self.footerHeight
        )

        self.listener.listen(self.cancelButton.onClick, lambda _: self.destroy())

    def search(self, address: str) -> None:
        if self.resultsComponent:
            self.resultsComponent.destroy()
            self.resultsComponent = None

        print("Searching", address)

        results = self.ctx.appContext.services.locations.search(
            address=address,
            limit=self.resultsLimit(),
        )

        if results is None:
            self.resultsComponent = ErrorResultComponent(
                ctx=self.ctx,
                root=self.topLeft,
                top=self.headerHeight,
                message="Error connecting to location service",
            )
        elif len(results) < 1:
            self.resultsComponent = ErrorResultComponent(
                ctx=self.ctx,
                root=self.topLeft,
                top=self.headerHeight,
                message="Location not found",
            )
        else:
            self.resultsComponent = self.handleSearchResult(results)

        self.updateSize(
            UIConstants.addressModalWidth,
            self.headerHeight + self.footerHeight + self.resultsComponent.height(),
        )

    @abstractmethod
    def resultsLimit(self) -> int:
        pass

    @abstractmethod
    def handleSearchResult(self, results: List[Location]) -> AddressResultsComponent:
        pass

    def destroy(self) -> None:
        super().destroy()
        self.listener.destroy()

        self.title.destroy()
        self.detailText.destroy()
        self.searchbar.destroy()
        self.cancelButton.destroy()

        if self.resultsComponent:
            self.resultsComponent.destroy()
