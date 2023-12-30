from lib.app.events import AppEvents
from lib.ui.context import UIContext

from ..core.modal import Modal


class StationSearchModal(Modal):
    def __init__(self, ctx: UIContext, events: AppEvents):
        super().__init__(ctx, events, 1, 1)
