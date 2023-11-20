from direct.showbase.ShowBase import ShowBase

from lib.app.app import App

if __name__ == "__main__":
    base = ShowBase()
    app = App(base)
    base.run()
