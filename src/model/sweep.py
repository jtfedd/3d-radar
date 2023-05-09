from model.ray import Ray


class Sweep:
    @classmethod
    def fromLevel2Data(cls, level2Sweep):
        rays = []

        for ray in level2Sweep:
            rays.append(Ray.fromLevel2Data(ray))

        return cls(rays)

    def __init__(self, rays):
        self.rays = rays

    def foreach(self, f):
        for ray in self.rays:
            ray.foreach(f)
