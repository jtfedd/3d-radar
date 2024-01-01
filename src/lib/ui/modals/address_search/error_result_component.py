from __future__ import annotations

from panda3d.core import NodePath, PandaNode

from lib.ui.context import UIContext
from lib.ui.core.constants import UIConstants

from ..core.text import ModalText
from .results_component import AddressResultsComponent


class ErrorResultComponent(AddressResultsComponent):
    def __init__(
        self,
        ctx: UIContext,
        root: NodePath[PandaNode],
        top: float,
        message: str,
    ):
        self.text = ModalText(ctx, root, top + UIConstants.modalPadding, message)

    def height(self) -> float:
        return self.text.height() + UIConstants.modalPadding

    def destroy(self) -> None:
        self.text.destroy()
