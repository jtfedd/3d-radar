from src.model.data_point import DataPoint
from src.model.ray_header import RayHeader
from src.model.reflectivity_header import ReflectivityHeader
from src.model.ray import Ray
from src.model.sweep import Sweep
from src.model.scan import Scan
import random
import datetime

def randomBytes(x):
    return bytearray(random.randbytes(x))

def newTestDataPoint(x=1, y=2, z=3, reflectivity=100):
    return DataPoint(x, y, z, reflectivity)

def newTestRayHeader(azimuth=1, elevation=2):
    return RayHeader(azimuth, elevation)

def newTestReflectivityHeader(numGates=5, gateWidth=0.1, firstGate=1.5):
    return ReflectivityHeader(numGates, gateWidth, firstGate)

def newTestRay(numPoints = 10, salt=1):
    header = newTestRayHeader(1*salt, 2*salt)
    reflectivityHeader = newTestReflectivityHeader(5+salt, 0.1*salt, 1.5+salt)
    points = []
    for i in range(numPoints):
        points.append(newTestDataPoint(reflectivity=3+i*salt))
    return Ray(header, reflectivityHeader, points)

def newTestSweep(numRays = 10, salt = 1):
    rays = []
    for i in range(numRays):
        rays.append(newTestRay(salt=i+salt))
    return Sweep(rays)

def newTestScan(numSweeps = 10, salt = 1):
    date = datetime.date(year=2005+salt, month=(3+salt)%12+1, day=(7*salt)%28+1)
    time = datetime.time(hour=(5+salt)%12+1, minute=(11*salt)%60, second=(13*salt)%60+1)
    station = random.choice(['KDMX', 'KAMX'])

    sweeps = []
    for i in range(numSweeps):
        sweeps.append(newTestSweep(salt=i+salt))
    return Scan(sweeps, station, date, time)
