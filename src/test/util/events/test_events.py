import unittest

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

        event.send(2)
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
