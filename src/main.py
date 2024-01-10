from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFileData

from lib.app.app import App

if __name__ == "__main__":
    loadPrcFileData("", "gl-version 3 2")
    base = ShowBase()
    app = App(base)
    base.run()
