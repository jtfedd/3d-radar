from model.ray import Ray
import numpy as np

import unittest


class TestDataPoint(unittest.TestCase):
    def test_range(self):
        ray = Ray(0, 0, 0.5, 1.6, [])

        self.assertEqual(ray.range(0), 0.5)
        self.assertEqual(ray.range(1), 2.1)
        self.assertEqual(ray.range(10), 16.5)

    def test_foreach(self):
        ray = Ray(1, 0.2, 1, 1, np.asarray([1, 2, np.nan, 3]))

        collectedPoints = []
        ray.foreach(lambda p: collectedPoints.append(p))

        self.assertEqual(len(collectedPoints), 3)

        self.assertAlmostEqual(collectedPoints[0].x, 0.8246975884333746)
        self.assertAlmostEqual(collectedPoints[0].y, 0.5295322319119196)
        self.assertAlmostEqual(collectedPoints[0].z, 0.19866933079506122)
        self.assertAlmostEqual(collectedPoints[0].value, 1)

        self.assertAlmostEqual(collectedPoints[1].x, 1.6493951768667492)
        self.assertAlmostEqual(collectedPoints[1].y, 1.0590644638238391)
        self.assertAlmostEqual(collectedPoints[1].z, 0.39733866159012243)
        self.assertAlmostEqual(collectedPoints[1].value, 2)

        self.assertAlmostEqual(collectedPoints[2].x, 3.2987903537334984)
        self.assertAlmostEqual(collectedPoints[2].y, 2.1181289276476782)
        self.assertAlmostEqual(collectedPoints[2].z, 0.7946773231802449)
        self.assertAlmostEqual(collectedPoints[2].value, 3)
