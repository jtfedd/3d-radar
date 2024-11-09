from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFile

from lib.app.app import App

if __name__ == "__main__":
    loadPrcFile("config/app.prc")
    loadPrcFile("config/logging.prc")

    base = ShowBase()
    app = App(base)
    base.run()
