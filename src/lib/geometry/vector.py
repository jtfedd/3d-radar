import numpy as np


def unitVector(vector):
    return vector / np.linalg.norm(vector)


def angle(v1, v2):
    v1Unit = unitVector(v1)
    v2Unit = unitVector(v2)
    return np.arccos(np.dot(v1Unit, v2Unit))
