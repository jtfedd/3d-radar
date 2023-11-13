from lib.ui.core.config import UIConfig
from lib.ui.panels.components.panel_buttons import PanelButtons
from lib.ui.panels.components.panel_content import PanelContent
from lib.ui.panels.panel_events import PanelEvents
from lib.ui.panels.panel_type import PanelType


class PanelModule:
    def __init__(self, config: UIConfig) -> None:
        self.config = config
        self.events = PanelEvents()

        self.panelType = PanelType.NONE
        self.panelContent: PanelContent | None = None

        self.buttons = PanelButtons(config, self.events)
        self.buttonsSub = self.buttons.onClick.listen(self.panelTypeClicked)

    def panelTypeClicked(self, newPanelType: PanelType) -> None:
        if self.panelType == PanelType.NONE and newPanelType == PanelType.NONE:
            return

        if newPanelType in (PanelType.NONE, self.panelType):
            self.closePanel()
        else:
            self.openPanel(newPanelType)

    def closePanel(self) -> None:
        self.panelType = PanelType.NONE
        self.destroyPanelContent()

        self.events.panelChanged.send(self.panelType)

    def openPanel(self, panel: PanelType) -> None:
        self.destroyPanelContent()

        # TODO create new panel content

        self.panelType = panel
        self.events.panelChanged.send(self.panelType)

    def destroyPanelContent(self) -> None:
        if self.panelContent:
            self.panelContent.destroy()
            self.panelContent = None

    def destroy(self) -> None:
        self.events.destroy()
        self.buttons.destroy()
        self.buttonsSub.cancel()
        self.destroyPanelContent()
