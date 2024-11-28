from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from panda3d.core import NodePath, PandaNode

from lib.app.context import AppContext
from lib.ui.core.components.background_card import BackgroundCard
from lib.ui.core.components.text import Text


class ContextMenuItem(ABC):
    @abstractmethod
    def renderText(self, ctx: AppContext, root: NodePath[PandaNode]) -> List[Text]:
        pass

    def renderLeftCap(self, _: NodePath[PandaNode]) -> BackgroundCard | None:
        return None

    @abstractmethod
    def onClick(self) -> None:
        pass
