from src.model.ray import Ray

class Sweep:
    def __init__(self, level2Sweep):
        self.rays = []

        for ray in level2Sweep:
            self.rays.append(Ray(ray))

    def foreach(self, f):
        for ray in self.rays:
            ray.foreach(f)
        