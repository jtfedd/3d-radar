from panda3d.core import DynamicTextFont


class UIFonts:
    def __init__(self) -> None:
        # https://fonts.google.com/specimen/Inter
        self.thin = DynamicTextFont("assets/font/Inter/Inter-Thin.ttf")
        self.light = DynamicTextFont("assets/font/Inter/Inter-Light.ttf")
        self.regular = DynamicTextFont("assets/font/Inter/Inter-Regular.ttf")
        self.medium = DynamicTextFont("assets/font/Inter/Inter-Medium.ttf")
        self.bold = DynamicTextFont("assets/font/Inter/Inter-Bold.ttf")
        self.black = DynamicTextFont("assets/font/Inter/Inter-Black.ttf")

        # https://fonts.google.com/specimen/Roboto+Mono
        self.mono = DynamicTextFont("assets/font/Roboto_Mono/RobotoMono-Regular.ttf")
