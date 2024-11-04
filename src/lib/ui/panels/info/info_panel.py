import webbrowser

from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.ui.context import UIContext
from lib.ui.core.constants import UIConstants
from lib.ui.panels.components.button import PanelButton
from lib.ui.panels.components.spacer import SpacerComponent
from lib.ui.panels.components.text import PanelText
from lib.ui.panels.components.title import TitleComponent
from lib.ui.panels.core.panel_content import PanelContent
from lib.util.events.listener import Listener


class InfoPanel(PanelContent):
    def __init__(self, ctx: UIContext, state: AppState, events: AppEvents) -> None:
        super().__init__(ctx, state, events)

        self.listener = Listener()

        self.addComponent(SpacerComponent(self.root))

        self.addComponent(PanelText(self.root, ctx, "3D Radar Viewer", bold=True))
        self.addComponent(PanelText(self.root, ctx, "v0.0.0"))
        self.addComponent(SpacerComponent(self.root))
        self.licenseButton = self.addComponent(
            PanelButton(self.root, ctx, "View License")
        )
        self.addComponent(SpacerComponent(self.root))

        self.addComponent(TitleComponent(self.root, ctx, "Credits"))

        self.addComponent(PanelText(self.root, ctx, "Radar Data:", bold=True))
        self.addComponent(SpacerComponent(self.root, UIConstants.labelPadding))
        self.awsButton = self.addComponent(PanelButton(self.root, ctx, "NEXRAD on AWS"))
        self.addComponent(SpacerComponent(self.root))

        self.addComponent(PanelText(self.root, ctx, "Stations and Alerts:", bold=True))
        self.addComponent(SpacerComponent(self.root, UIConstants.labelPadding))
        self.nwsButton = self.addComponent(
            PanelButton(self.root, ctx, "National Weather Service API")
        )
        self.addComponent(SpacerComponent(self.root))

        self.addComponent(
            PanelText(self.root, ctx, "Cartographic Boundary Files:", bold=True)
        )
        self.addComponent(SpacerComponent(self.root, UIConstants.labelPadding))
        self.censusBureauButton = self.addComponent(
            PanelButton(self.root, ctx, "United States Census Bureau")
        )
        self.addComponent(SpacerComponent(self.root))

        self.addComponent(PanelText(self.root, ctx, "Location Search:", bold=True))
        self.addComponent(SpacerComponent(self.root, UIConstants.labelPadding))
        self.openStreetMapButton = self.addComponent(
            PanelButton(self.root, ctx, "OpenStreetMap")
        )
        self.addComponent(SpacerComponent(self.root))

        self.addComponent(PanelText(self.root, ctx, "Fonts:", bold=True))
        self.addComponent(SpacerComponent(self.root, UIConstants.labelPadding))
        self.interButton = self.addComponent(PanelButton(self.root, ctx, "Inter"))
        self.addComponent(SpacerComponent(self.root, UIConstants.labelPadding))
        self.robotoMonoButton = self.addComponent(
            PanelButton(self.root, ctx, "Roboto Mono")
        )
        self.addComponent(SpacerComponent(self.root))

        self.addComponent(PanelText(self.root, ctx, "Icons:", bold=True))
        self.addComponent(SpacerComponent(self.root, UIConstants.labelPadding))
        self.iconsButton = self.addComponent(PanelButton(self.root, ctx, "Icons8"))
        self.addComponent(SpacerComponent(self.root))

        self.listener.listen(
            self.licenseButton.button.onClick,
            events.ui.modals.license.send,
        )

        self.bind(
            self.awsButton,
            "https://registry.opendata.aws/noaa-nexrad",
        )
        self.bind(
            self.nwsButton,
            "https://www.weather.gov/documentation/services-web-api",
        )
        self.bind(
            self.censusBureauButton,
            "https://www.census.gov/geographies/mapping-files/time-series/"
            + "geo/cartographic-boundary.html",
        )
        self.bind(
            self.openStreetMapButton,
            "https://www.openstreetmap.org/copyright",
        )
        self.bind(
            self.interButton,
            "https://fonts.google.com/specimen/Inter",
        )
        self.bind(
            self.robotoMonoButton,
            "https://fonts.google.com/specimen/Roboto+Mono",
        )
        self.bind(
            self.iconsButton,
            "https://icons8.com/icons",
        )

    def bind(self, button: PanelButton, url: str) -> None:
        self.listener.listen(
            button.button.onClick,
            lambda _: self.openUrl(url),
        )

    def openUrl(self, url: str) -> None:
        webbrowser.open(url)

    def headerText(self) -> str:
        return "About"

    def destroy(self) -> None:
        super().destroy()

        self.listener.destroy()
