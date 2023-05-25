from lib.model.scan import Scan
from test.testutils.models import newTestScan

import datetime
import unittest


class TestSweep:
    def __init__(self):
        self.foreachCalled = False
        self.foreachCalledWith = None
        self.elevation = 0

    def foreach(self, f):
        self.foreachCalled = True
        self.foreachCalledWith = f


class TestScan(unittest.TestCase):
    def test_foreach(self):
        sweeps = [TestSweep() for _ in range(10)]
        scan = Scan(sweeps, "KABC", datetime.date(2023, 5, 2), datetime.time(5, 40, 23))

        def myfunc(p):
            pass

        scan.foreach(myfunc)

        for sweep in sweeps:
            self.assertTrue(sweep.foreachCalled)
            self.assertEqual(sweep.foreachCalledWith, myfunc)

    def test_points(self):
        scan = newTestScan()
        points = scan.points()
        self.assertEqual(len(points), 1000)
