import unittest
from functools import cmp_to_key

from lib.model.location import Location
from lib.model.location_query import LocationQuery, compareLocationQueries


class TestLocationQuery(unittest.TestCase):
    def testComparator(self) -> None:
        a = LocationQuery("asdf", 2, [])
        b = LocationQuery("asdf", 2, [Location("Hi", "There", 0, 0)])
        c = LocationQuery("asdf", 3, [])
        d = LocationQuery("fdsa", 1, [])

        self.assertEqual(compareLocationQueries(a, a), 0)
        self.assertEqual(compareLocationQueries(a, b), 0)
        self.assertEqual(compareLocationQueries(a, c), -1)
        self.assertEqual(compareLocationQueries(c, a), 1)
        self.assertEqual(compareLocationQueries(a, d), -1)
        self.assertEqual(compareLocationQueries(d, a), 1)

    def testSort(self) -> None:
        a = LocationQuery("asdf", 2, [])
        b = LocationQuery("qwert", 2, [Location("Hi", "There", 0, 0)])
        c = LocationQuery("asdf", 3, [])
        d = LocationQuery("fdsa", 1, [])

        self.assertListEqual(
            sorted([a, b, c, d], key=cmp_to_key(compareLocationQueries)),
            [a, c, d, b],
        )
