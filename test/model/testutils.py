from src.model.data_point import DataPoint
from src.model.ray_header import RayHeader
from src.model.reflectivity_header import ReflectivityHeader
from src.model.ray import Ray
import random

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
