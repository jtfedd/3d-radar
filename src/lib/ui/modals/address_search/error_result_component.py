from __future__ import annotations

from panda3d.core import NodePath, PandaNode

from lib.app.context import AppContext

from ..core.text import ModalText
from .results_component import AddressResultsComponent


class ErrorResultComponent(AddressResultsComponent):
    def __init__(
        self,
        ctx: AppContext,
        root: NodePath[PandaNode],
        top: float,
        message: str,
    ):
        self.text = ModalText(ctx, root, top, message)

    def height(self) -> float:
        return self.text.height()

    def destroy(self) -> None:
        self.text.destroy()
