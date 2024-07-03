from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFileData

from lib.app.app import App

CONFIG = """
gl-version 3 2
window-title Stormfront 3D Radar Viewer
icon-filename assets/icon/icon.ico
paste-emit-keystrokes false
"""

if __name__ == "__main__":
    loadPrcFileData("", CONFIG)

    base = ShowBase()
    app = App(base)
    base.run()
