from __future__ import annotations

from panda3d.core import NodePath, PandaNode

from lib.ui.context import UIContext

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
        self.text = ModalText(ctx, root, top, message)

    def height(self) -> float:
        return self.text.height()

    def destroy(self) -> None:
        self.text.destroy()
