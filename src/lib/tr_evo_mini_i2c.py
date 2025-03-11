from machine import UART
from time import sleep_ms


class EvoMini:
    TEXT_MODE = "\x00\x11\x01\x45"
    BINARY_MODE = "\x00\x01\x02\x4c"
    PIXEL_MODE_1PX = "\x00\x21\x01\xbc"
    PIXEL_MODE_2PX = "\x00\x21\x03\xb2"
    PIXEL_MODE_4PX = "\x00\x21\x02\xb5"
    SHORT_RANGE_MODE = "\x00\x61\x01\xe7"
    LONG_RANGE_MODE = "\x00\x61\x03\xe9"

    def __init__(self, port: int):
        self._uart = UART(port, 115200)
        self._uart.init(115200, bits=8, parity=None, stop=1, timeout=500)
        sleep_ms(100)

    def config(self):
        self._write(self.TEXT_MODE)
        self._write(self.PIXEL_MODE_4PX)
        self._write(self.LONG_RANGE_MODE)

    def read_range(self) -> float:
        """Read the sensor and calculate the distance

        Raises:
            ValueError: Bad string
            ValueError: Not enough fields returned

        Returns:
            float: Distance in cm
        """
        self._uart.flush()

        range = self._read()

        if type(range) is not str:
            raise ValueError("No response")

        range = range.strip()
        range = range.split(",")

        if len(range) < 4:
            raise ValueError(f"{len(range)} out of 4 readings reported")

        range = [int(r) for r in range]
        ave_range_mm = sum(range) / 4

        return ave_range_mm / 10  # Return cm

    def _write(self, msg: str):
        print(self._uart.write(msg + "\n"))

    def _read(self) -> str | None:
        return self._uart.readline()
