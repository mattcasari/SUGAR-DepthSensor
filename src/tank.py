import math
from lib.tr_evo_mini_i2c import EvoMini


class TankVolume:
    RADIUS = 100  # cm
    CONE_MAX_HEIGHT = 50  # cm
    CYLINDER_MAX_HEIGHT = 50

    def __init__(self, get_distance: function, mounted_distance: float):
        self.get_distance = get_distance
        self._mounted_distance = mounted_distance

    def get_volume(self):
        depth = self._mounted_distance - self.get_distance()

        if depth > self.CONE_MAX_HEIGHT:
            volume = self._cylinder_volume(depth - self.CONE_MAX_HEIGHT)
            volume += self._cone_volume(self.CONE_MAX_HEIGHT)
        else:
            volume = self._cone_volume(depth)

        return volume

    def _cone_volume(self, height: float):
        # V=πr2h/3
        return math.pi * (self.RADIUS**2) * height / 3

    def _cylinder_volume(self, height: float):
        return math.pi * (self.RADIUS**2) * height
