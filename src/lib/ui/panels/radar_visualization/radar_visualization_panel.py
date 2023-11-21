from lib.ui.core.context import UIContext
from lib.ui.panels.components.panel_spacer import PanelSpacer
from lib.ui.panels.core.panel_content import PanelContent


class RadarVisualizationPanel(PanelContent):
    def __init__(self, ctx: UIContext) -> None:
        super().__init__(ctx)

        self.addComponent(PanelSpacer(self.root))

    def headerText(self) -> str:
        return "Radar Visualization"

    def destroy(self) -> None:
        super().destroy()
