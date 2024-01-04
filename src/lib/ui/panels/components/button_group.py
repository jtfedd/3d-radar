from __future__ import annotations

from typing import Callable, Generic, List, Tuple, TypeVar

from panda3d.core import NodePath, PandaNode

from lib.ui.context import UIContext
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.components.button import Button, ButtonSkin
from lib.ui.core.constants import UIConstants
from lib.ui.panels.components.label import ComponentLabel
from lib.util.events.listener import Listener
from lib.util.events.observable import Observable

from ..core.panel_component import PanelComponent

T = TypeVar("T")


class PanelButtonGroup(PanelComponent, Generic[T]):
    def __init__(
        self,
        root: NodePath[PandaNode],
        ctx: UIContext,
        observable: Observable[T],
        buttonDefs: List[Tuple[str, T]],
        label: str | None = None,
        left: float = 0.0,
        height: float = UIConstants.panelButtonGroupHeight,
    ):
        super().__init__(root)
        self.listener = Listener()

        self.observable = observable
        self.buttons: List[Button] = []
        self.buttonDefs = buttonDefs

        self.label: ComponentLabel | None = None
        if label:
            self.label = ComponentLabel(self.root, ctx, label)

        buttonWidth = (UIConstants.panelContentWidth - left) / len(buttonDefs)
        for i, buttonDef in enumerate(buttonDefs):
            button = Button(
                self.root,
                ctx,
                width=buttonWidth,
                height=height,
                x=UIConstants.panelPadding + left + i * buttonWidth,
                y=0,
                hAlign=HAlign.LEFT,
                vAlign=VAlign.TOP,
                toggleState=observable.value == buttonDef[1],
                text=buttonDef[0],
                skin=ButtonSkin.ACCENT,
            )

            self.listener.listen(button.onClick, self.handleButtonClick(buttonDef[1]))

            self.buttons.append(button)

        self.listener.listen(observable, lambda _: self.updateButtonStates())

    def handleButtonClick(self, value: T) -> Callable[[None], None]:
        return lambda _: self.observable.setValue(value)

    def updateButtonStates(self) -> None:
        for i, button in enumerate(self.buttons):
            button.setToggleState(self.observable.value == self.buttonDefs[i][1])

    def getHeight(self) -> float:
        return UIConstants.panelButtonGroupHeight

    def destroy(self) -> None:
        super().destroy()

        self.listener.destroy()

        if self.label:
            self.label.destroy()

        for button in self.buttons:
            button.destroy()
