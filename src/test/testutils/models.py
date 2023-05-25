from lib.model.data_point import DataPoint
from lib.model.ray import Ray
from lib.model.sweep import Sweep
from lib.model.scan import Scan
import random
import datetime
import numpy as np

import unittest


def newTestRay(numPoints=10, salt=1):
    return Ray(
        0.2 * salt,
        5 + salt,
        0.5 * salt,
        np.random.uniform(low=-30, high=70, size=(numPoints,)),
    )


def newTestSweep(numRays=10, salt=1):
    rays = []
    for i in range(numRays):
        rays.append(newTestRay(salt=i + salt))
    return Sweep(0.3 * salt, rays)


def newTestScan(numSweeps=10, salt=1):
    date = datetime.date(
        year=2005 + salt, month=(3 + salt) % 12 + 1, day=(7 * salt) % 28 + 1
    )
    time = datetime.time(
        hour=(5 + salt) % 12 + 1, minute=(11 * salt) % 60, second=(13 * salt) % 60 + 1
    )
    station = random.choice(["KDMX", "KAMX"])

    sweeps = []
    for i in range(numSweeps):
        sweeps.append(newTestSweep(salt=i + salt))
    return Scan(sweeps, station, date, time)


def assertRaysEqual(t: unittest.TestCase, first: Ray, second: Ray):
    t.assertIsInstance(first, Ray)
    t.assertIsInstance(second, Ray)

    t.assertAlmostEqual(first.azimuth, second.azimuth)
    t.assertAlmostEqual(first.first, second.first)
    t.assertAlmostEqual(first.spacing, second.spacing)

    t.assertEqual(len(first.reflectivity), len(second.reflectivity))
    for i in range(len(first.reflectivity)):
        firstValue = first.reflectivity[i]
        secondValue = second.reflectivity[i]

        t.assertEqual(np.isnan(firstValue), np.isnan(secondValue))
        if np.isnan(firstValue):
            continue

        t.assertAlmostEqual(firstValue, secondValue)


def assertSweepsEqual(t: unittest.TestCase, first: Sweep, second: Sweep):
    t.assertIsInstance(first, Sweep)
    t.assertIsInstance(second, Sweep)

    t.assertAlmostEqual(first.elevation, second.elevation)

    t.assertEqual(len(first.rays), len(second.rays))

    for i in range(len(first.rays)):
        assertRaysEqual(t, first.rays[i], second.rays[i])


def assertScansEqual(t: unittest.TestCase, first: Scan, second: Scan):
    t.assertIsInstance(first, Scan)
    t.assertIsInstance(second, Scan)

    t.assertEqual(first.date, second.date)
    t.assertEqual(first.time, second.time)
    t.assertEqual(first.station, second.station)
    t.assertEqual(len(first.sweeps), len(second.sweeps))

    for i in range(len(first.sweeps)):
        assertSweepsEqual(t, first.sweeps[i], second.sweeps[i])
