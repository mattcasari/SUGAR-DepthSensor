from time import sleep_ms
from src.lib.tr_evo_mini_i2c import EvoMini
from src.tank import TankVolume


def main():
    ds = EvoMini(1)
    tank = TankVolume(ds.read_range, 1000)

    while True:
        try:
            volume = tank.get_volume()
            print(f"Volume: {range} mm")
        except ValueError as e:
            print(f"Error in read.  Message was: {e}")
        except Exception as e:
            print(e)
        finally:
            sleep_ms(1000)


if __name__ == "__main__":
    main()
