from __future__ import annotations

from panda3d.core import NodePath, PandaNode

from lib.ui.context import UIContext
from lib.ui.core.alignment import HAlign
from lib.ui.core.components.button import Button, ButtonSkin
from lib.ui.core.constants import UIConstants
from lib.ui.core.icons import Icons
from lib.ui.panels.components.label import ComponentLabel
from lib.ui.panels.core.panel_component import PanelComponent
from lib.util.events.listener import Listener
from lib.util.events.observable import Observable


class CheckboxComponent(PanelComponent):
    def __init__(
        self,
        root: NodePath[PandaNode],
        ctx: UIContext,
        label: str,
        observable: Observable[bool],
    ):
        super().__init__(root)

        self.listener = Listener()

        self.checkbox = Button(
            self.root,
            ctx,
            width=UIConstants.checkboxSize,
            height=UIConstants.checkboxSize,
            x=UIConstants.panelPadding + UIConstants.checkboxPadding,
            y=-UIConstants.panelInputHeight / 2,
            hAlign=HAlign.LEFT,
            toggleState=observable.value,
            icon=Icons.CHECKBOX,
            toggleIcon=Icons.CHECKMARK,
            iconWidth=UIConstants.checkboxSize,
            iconHeight=UIConstants.checkboxSize,
            skin=ButtonSkin.DARK,
            toggleSkin=ButtonSkin.DARK,
        )

        self.label = ComponentLabel(
            self.root,
            ctx,
            label,
            left=UIConstants.checkboxSize + UIConstants.checkboxPadding * 2,
        )

        self.listener.listen(
            self.checkbox.onClick,
            lambda _: observable.setValue(not observable.value),
        )

        self.listener.listen(observable, self.checkbox.setToggleState)

    def getHeight(self) -> float:
        return UIConstants.panelInputHeight

    def destroy(self) -> None:
        super().destroy()

        self.listener.destroy()

        self.label.destroy()
        self.checkbox.destroy()
