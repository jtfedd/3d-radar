from direct.showbase.DirectObject import DirectObject
from panda3d.core import NodePath, PandaNode

from lib.ui.core.params import UIParams


class Footer(DirectObject):
    def __init__(self, root: NodePath[PandaNode], params: UIParams):
        self.params = params
