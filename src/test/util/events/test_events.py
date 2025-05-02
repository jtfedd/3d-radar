import unittest

from lib.util.errors import StateError
from lib.util.events.event_dispatcher import EventDispatcher


class TestEvents(unittest.TestCase):
    def testEvent(self) -> None:
        event = EventDispatcher[int]()

        x = 0

        def incrementX(value: int) -> None:
            nonlocal x
            x += value

        subscription = event.listen(incrementX)

        self.assertEqual(x, 0)
        event.send(5)
        self.assertEqual(x, 5)
        event.send(10)
        self.assertEqual(x, 15)

        subscription.cancel()

        event.send(3)
        self.assertEqual(x, 15)

    def testEventMultipleSubscriptions(self) -> None:
        event = EventDispatcher[int]()

        x = 0
        y = 0

        def incrementX(value: int) -> None:
            nonlocal x
            x += value

        def incrementY(value: int) -> None:
            nonlocal y
            y += value

        subscriptionX = event.listen(incrementX)

        self.assertEqual(x, 0)
        self.assertEqual(y, 0)

        event.send(5)

        self.assertEqual(x, 5)
        self.assertEqual(y, 0)

        subscriptionY = event.listen(incrementY)

        event.send(7)

        self.assertEqual(x, 12)
        self.assertEqual(y, 7)

        subscriptionX.cancel()

        event.send(2)

        self.assertEqual(x, 12)
        self.assertEqual(y, 9)

        subscriptionY.cancel()

        event.send(2)

        self.assertEqual(x, 12)
        self.assertEqual(y, 9)

    def testEventInteractingAfterCloseRaisesErrors(self) -> None:
        event = EventDispatcher[int]()

        event.close()

        def callback(_: int) -> None:
            pass

        # Calling close again should raise an exception
        self.assertRaises(StateError, event.close)
        self.assertRaises(StateError, event.listen, callback)
        self.assertRaises(StateError, event.send, 1)

    def testEventSubscriptionsCancelledAfterEventClosed(self) -> None:
        event = EventDispatcher[int]()

        def callback(_: int) -> None:
            pass

        subscription = event.listen(callback)

        event.close()
        subscription.cancel()

    def testEventSubscriptionInteractingAfterCloseRaisesError(self) -> None:
        event = EventDispatcher[int]()

        def callback(_: int) -> None:
            pass

        subscription = event.listen(callback)

        subscription.cancel()

        self.assertRaises(StateError, subscription.cancel)
        self.assertRaises(StateError, subscription.send, 1)
