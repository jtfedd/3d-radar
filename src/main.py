from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFileData

from lib.app.app import App

# TODO for mac support
# - [ ] Custom shader for 3-d markers
# - [ ] Custom shader for map
#   - [x] Clip planes
#   - [ ] Line thickness

CONFIG = """
gl-version 3 2
window-title Stormfront 3D Radar Viewer
icon-filename assets/icon/icon.ico
"""

if __name__ == "__main__":
    loadPrcFileData("", CONFIG)

    base = ShowBase()
    app = App(base)
    base.run()
