from abc import ABC, abstractmethod
from typing import List

from lib.app.context import AppContext
from lib.app.events import AppEvents
from lib.model.location import Location
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.components.text_input import TextInput
from lib.ui.core.constants import UIConstants
from lib.ui.core.layers import UILayer
from lib.util.events.listener import Listener

from ..core.footer_button import FooterButton
from ..core.modal import Modal
from ..core.text import ModalText
from ..core.title import ModalTitle
from .error_result_component import ErrorResultComponent
from .results_component import AddressResultsComponent


class AddressSearchModal(Modal, ABC):
    def __init__(
        self, ctx: AppContext, events: AppEvents, title: str, description: str
    ):
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

        self.cancelButton = FooterButton(
            ctx,
            self.bottomLeft,
            UIConstants.addressModalWidth,
            "Cancel",
        )

        self.headerHeight = top
        self.footerHeight = (
            UIConstants.modalFooterButtonHeight + UIConstants.modalPadding
        )

        self.resultsComponent: AddressResultsComponent | None = None

        self.updateSize(
            UIConstants.addressModalWidth, self.headerHeight + self.footerHeight
        )

        self.listener.listen(self.cancelButton.button.onClick, lambda _: self.destroy())

    def search(self, address: str) -> None:
        if self.resultsComponent:
            self.resultsComponent.destroy()
            self.resultsComponent = None

        results = self.ctx.services.locations.search(
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
