import unittest

from lib.util.errors import StateError
from lib.util.observable.observable import Observable


class TestObservable(unittest.TestCase):
    def testObservable(self) -> None:
        ob = Observable[int](5)

        self.assertEqual(ob.getValue(), 5)
        ob.setValue(10)
        self.assertEqual(ob.getValue(), 10)

        x = 0

        def incrementX(value: int) -> None:
            nonlocal x
            x += value

        sub = ob.listen(incrementX)

        ob.setValue(2)
        self.assertEqual(x, 2)
        self.assertEqual(ob.getValue(), 2)

        ob.setValue(7)
        self.assertEqual(x, 9)
        self.assertEqual(ob.getValue(), 7)

        sub.cancel()

        ob.setValue(3)
        self.assertEqual(x, 9)
        self.assertEqual(ob.getValue(), 3)

        ob.close()

        self.assertRaises(StateError, ob.setValue, 9)
