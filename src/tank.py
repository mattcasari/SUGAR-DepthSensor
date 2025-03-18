import math


class TankVolume:
    RADIUS = 97.79  # cm
    CONE_MAX_HEIGHT = 121.6  # cm
    CYLINDER_MAX_HEIGHT = 85.46  # cm

    TOTAL_VOLUME = 3785.41  # liters
    TOTAL_VOLUME_CM3 = TOTAL_VOLUME * 1000

    def __init__(self, get_distance: function, mounted_distance: float):
        """_summary_

        Args:
            get_distance (function): Function that reads the distance sensor distance
            mounted_distance (float): Distance sensor is mounted from bottom of tank (cm)
        """
        self.get_distance = get_distance
        self._mounted_distance = mounted_distance

    def get_volume(self):
        """Get the current tank volume

        Returns:
            float: Tank volume (cm3)
        """
        try:
            distance = self.get_distance()
            depth = self._mounted_distance - distance
        except ValueError as e:
            print(f"Error in read.  Message was: {e}")
            return -1
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        volume = self._calculate_combined_volume(depth=depth)

        if volume < 0.0:
            return 0

        if volume < self.TOTAL_VOLUME_CM3:
            return volume

        return self.TOTAL_VOLUME_CM3

    def get_volume_gallons(self):
        return self.get_volume() * 0.000264172

    def get_volume_liters(self):
        return self.get_volume() * 0.001

    def _cone_volume(self, height: float):
        # V=πr2h/3
        return math.pi * (self.RADIUS**2) * height / 3

    def _cylinder_volume(self, height: float):
        return math.pi * (self.RADIUS**2) * height

    def _calculate_combined_volume(self, depth: float):
        if depth > self.CONE_MAX_HEIGHT:
            volume = self._cylinder_volume(depth - self.CONE_MAX_HEIGHT)
            volume += self._cone_volume(self.CONE_MAX_HEIGHT)
        else:
            volume = self._cone_volume(depth)

        return volume
