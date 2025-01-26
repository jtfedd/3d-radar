from lib.app.context import AppContext
from lib.app.state import AppState
from lib.renderer.surface_renderer import SurfaceRenderer
from lib.renderer.volume_renderer import VolumeRenderer
from lib.util.events.listener import Listener

from .provider.lighting_data_provider import LightingDataProvider
from .provider.volume_data_provider import VolumeDataProvider


class RenderManager(Listener):
    def __init__(self, ctx: AppContext, state: AppState) -> None:
        super().__init__()

        self.ctx = ctx
        self.state = state

        self.volumeDataProvider = VolumeDataProvider(ctx, state)
        self.lightingDataProvider = LightingDataProvider(ctx, state)

        self.volumeRenderer = VolumeRenderer(ctx, state)
        self.surfaceRenderer = SurfaceRenderer(ctx, state)

        self.volumeDataProvider.addNode(self.volumeRenderer.plane)
        self.volumeDataProvider.addNode(self.surfaceRenderer.surface)
        self.lightingDataProvider.addNode(self.volumeRenderer.plane)

    def destroy(self) -> None:
        super().destroy()

        self.volumeRenderer.destroy()
        self.surfaceRenderer.destroy()

        self.lightingDataProvider.destroy()
        self.volumeDataProvider.destroy()
