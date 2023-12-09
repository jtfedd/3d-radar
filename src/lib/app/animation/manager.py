from lib.app.events import AppEvents
from lib.util.events.listener import Listener
from lib.util.events.observable import Observable


class AnimationManager(Listener):
    def __init__(self, events: AppEvents) -> None:
        super().__init__()

        self.playing = Observable[bool](False)

        self.listen(
            events.animation.play,
            lambda _: self.playing.setValue(not self.playing.value),
        )

        self.listen(
            events.input.onPlay,
            lambda _: self.playing.setValue(not self.playing.value),
        )

        self.listen(events.animation.next, lambda _: self.playing.setValue(False))
        self.listen(events.animation.previous, lambda _: self.playing.setValue(False))
        self.listen(events.animation.slider, lambda _: self.playing.setValue(False))
        self.listen(events.requestData, lambda _: self.playing.setValue(False))

    def destroy(self) -> None:
        super().destroy()

        self.playing.close()
