from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Tuple

from panda3d.core import NodePath, PandaNode

from lib.app.events import AppEvents
from lib.ui.context import UIContext
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.components.scrollable_panel import ScrollablePanel
from lib.ui.core.constants import UIConstants
from lib.ui.core.layers import UILayer


class AddressResultsComponent(ABC):
    @abstractmethod
    def height(self) -> float:
        pass

    @abstractmethod
    def destroy(self) -> None:
        pass

    def setupButtonRoot(
        self,
        ctx: UIContext,
        events: AppEvents,
        top: float,
        contentHeight: float,
        buttonListHeight: float,
        root: NodePath[PandaNode],
    ) -> Tuple[ScrollablePanel | None, NodePath[PandaNode], float, float]:
        scroll: ScrollablePanel | None = None
        buttonTopOffset = top + contentHeight
        buttonRoot: NodePath[PandaNode]

        if buttonListHeight > UIConstants.addressModalResultButtonsMaxHeight:
            scroll = ScrollablePanel(
                root=root,
                ctx=ctx,
                events=events,
                y=-(top + contentHeight),
                width=UIConstants.addressModalWidth + UIConstants.modalPadding,
                height=UIConstants.addressModalResultButtonsMaxHeight,
                canvasHeight=buttonListHeight,
                hAlign=HAlign.LEFT,
                vAlign=VAlign.TOP,
                layer=UILayer.MODAL_CONTENT_INTERACTION,
                scrollbarPadding=UIConstants.modalScrollbarPadding,
            )
            contentHeight += UIConstants.addressModalResultButtonsMaxHeight
            buttonTopOffset = 0
            buttonRoot = scroll.getCanvas()
        else:
            contentHeight += buttonListHeight
            buttonRoot = root

        return (scroll, buttonRoot, contentHeight, buttonTopOffset)
