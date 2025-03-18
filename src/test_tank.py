from src.lib.tr_evo_mini_i2c import EvoMini
from src.tank import TankVolume
from time import sleep_ms


def main():

    ev = EvoMini(1, 8, 9)
    tank = TankVolume(ev.read_range, 210)

    while True:
        print(f"volume={tank.get_volume_gallons()} Gallons\n")
        # print(f"volume={tank.get_volume_liters()} liters")
        sleep_ms(1000)
