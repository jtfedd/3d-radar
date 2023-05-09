from model.sweep import Sweep

import unittest


class TestRay:
    def __init__(self):
        self.foreachCalled = False
        self.foreachCalledWith = None

    def foreach(self, f):
        self.foreachCalled = True
        self.foreachCalledWith = f


class TestSweep(unittest.TestCase):
    def test_foreach(self):
        rays = [TestRay() for _ in range(10)]
        sweep = Sweep(rays)

        def myfunc(p):
            pass

        sweep.foreach(myfunc)

        for ray in rays:
            self.assertTrue(ray.foreachCalled)
            self.assertEqual(ray.foreachCalledWith, myfunc)
