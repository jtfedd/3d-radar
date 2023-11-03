from panda3d.core import DynamicTextFont


class UIFonts:
    def __init__(self) -> None:
        # https://fonts.google.com/specimen/Inter
        self.thin = DynamicTextFont("assets/font/Inter-Thin.ttf", 0)
        self.extraLight = DynamicTextFont("assets/font/Inter-ExtraLight.ttf", 0)
        self.light = DynamicTextFont("assets/font/Inter-Light.ttf", 0)
        self.regular = DynamicTextFont("assets/font/Inter-Regular.ttf", 0)
        self.medium = DynamicTextFont("assets/font/Inter-Medium.ttf", 0)
        self.semiBold = DynamicTextFont("assets/font/Inter-SemiBold.ttf", 0)
        self.bold = DynamicTextFont("assets/font/Inter-Bold.ttf", 0)
        self.extraBold = DynamicTextFont("assets/font/Inter-ExtraBold.ttf", 0)
        self.black = DynamicTextFont("assets/font/Inter-Black.ttf", 0)
