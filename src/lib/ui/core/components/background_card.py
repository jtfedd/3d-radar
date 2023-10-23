from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import NodePath, PandaNode, Vec4

from lib.ui.core.layers import UILayer


class BackgroundCard:
    def __init__(
        self,
        root: NodePath[PandaNode],
        x: float,
        y: float,
        width: float,
        height: float,
        color: Vec4,
        layer: UILayer = UILayer.BACKGROUND,
    ) -> None:
        self.card = OnscreenImage(
            pos=(x + width / 2, 0, -(y + height / 2)),
            scale=(width, 1, height),
            parent=root,
            color=color,
            sort=layer.value,
        )

    def destroy(self) -> None:
        self.card.destroy()
