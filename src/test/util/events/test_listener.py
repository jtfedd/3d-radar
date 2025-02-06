import unittest

from lib.util.events.event_dispatcher import EventDispatcher
from lib.util.events.listener import Listener
from lib.util.events.observable import Observable


class TestListener(unittest.TestCase):
    def testListenerListen(self) -> None:
        listener = Listener()
        event = EventDispatcher[int]()

        x = 0

        def onEvent(value: int) -> None:
            nonlocal x
            x = value

        listener.listen(event, onEvent)

        event.send(10)
        self.assertEqual(x, 10)

        event.send(100)
        self.assertEqual(x, 100)

        listener.destroy()

        event.send(1000)
        self.assertEqual(x, 100)

    def testListenerBind(self) -> None:
        listener = Listener()
        observable = Observable[int](5)

        x = 0

        def onEvent(value: int) -> None:
            nonlocal x
            x = value

        listener.bind(observable, onEvent)
        self.assertEqual(x, 5)

        observable.send(10)
        self.assertEqual(x, 10)

        observable.send(100)
        self.assertEqual(x, 100)

        listener.destroy()

        observable.send(1000)
        self.assertEqual(x, 100)

    def testListenerTrigger(self) -> None:
        listener = Listener()
        event = EventDispatcher[None]()

        callCount = 0

        def onEvent() -> None:
            nonlocal callCount
            callCount += 1

        listener.trigger(event, onEvent)

        event.send(None)
        self.assertEqual(callCount, 1)

        event.send(None)
        self.assertEqual(callCount, 2)

        listener.destroy()

        event.send(None)
        self.assertEqual(callCount, 2)

    def testListenerTriggerMany(self) -> None:
        listener = Listener()
        event1 = EventDispatcher[None]()
        event2 = EventDispatcher[None]()

        callCount = 0

        def onEvent() -> None:
            nonlocal callCount
            callCount += 1

        listener.triggerMany([event1, event2], onEvent)

        event1.send(None)
        self.assertEqual(callCount, 1)

        event2.send(None)
        self.assertEqual(callCount, 2)

        event1.send(None)
        self.assertEqual(callCount, 3)

        listener.destroy()

        event1.send(None)
        event2.send(None)
        self.assertEqual(callCount, 3)
