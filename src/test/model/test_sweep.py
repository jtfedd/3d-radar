from lib.model.sweep import Sweep

import unittest
import math


class TestRay:
    def __init__(self):
        self.foreachCalled = False
        self.foreachCalledWith = None

    def foreach(self, e, f):
        self.foreachCalled = True
        self.foreachCalledWith = (e, f)


class TestSweep(unittest.TestCase):
    def test_foreach(self):
        rays = [TestRay() for _ in range(10)]
        sweep = Sweep(0.4, rays)

        def myfunc(p):
            pass

        sweep.foreach(myfunc)

        for ray in rays:
            self.assertTrue(ray.foreachCalled)
            self.assertEqual(ray.foreachCalledWith, (math.radians(0.4), myfunc))
