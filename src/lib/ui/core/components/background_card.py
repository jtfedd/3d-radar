from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import NodePath, PandaNode, Vec4


class BackgroundCard:
    def __init__(
        self,
        root: NodePath[PandaNode],
        x: float,
        y: float,
        width: float,
        height: float,
        color: Vec4,
    ) -> None:
        self.card = OnscreenImage(
            pos=(x + width / 2, 0, -(y + height / 2)),
            scale=(width, 1, height),
            parent=root,
            color=color,
        )

    def destroy(self) -> None:
        self.card.destroy()
