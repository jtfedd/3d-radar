from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFileData

from lib.app.app import App

if __name__ == "__main__":
    loadPrcFileData("", "window-title Stormfront 3D Radar Viewer")
    loadPrcFileData("", "icon-filename assets/icon/icon.ico")

    base = ShowBase()
    app = App(base)
    base.run()
