from machine import UART
from time import sleep_ms


class EvoMini:
    TEXT_MODE = b"\x00\x11\x01\x45"
    BINARY_MODE = b"\x00\x01\x02\x4c"
    PIXEL_MODE_1PX = b"\x00\x21\x01\xbc"
    PIXEL_MODE_2PX = b"\x00\x21\x03\xb2"
    PIXEL_MODE_4PX = b"\x00\x21\x02\xb5"
    SHORT_RANGE_MODE = b"\x00\x61\x01\xe7"
    LONG_RANGE_MODE = b"\x00\x61\x03\xe9"

    def __init__(self, port: int, tx: int, rx: int):
        self._uart = UART(port, baudrate=115200, tx=tx, rx=rx)
        self._uart.init(115200, bits=8, parity=None, stop=1, timeout=500)
        sleep_ms(100)
        self.config()

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

        range = self._read()

        if type(range) is not str:
            raise ValueError("No response")

        range = range.strip()
        range = range.split(",")
        # print(f"{range=}")

        # Remove +inf and -inf values
        range = [item for item in range if item is not "+Inf"]
        range = [item for item in range if item is not "-Inf"]

        # Remove None values from list
        range = [item for item in range if item is not None]

        # Convert the values to integers
        range = [int(r) for r in range]

        # Remove values of -1 from list
        range = [r for r in range if r != -1]

        # print(f"Final {range=}\n")

        if len(range) < 1:
            raise ValueError(f"No valid ranges reported")

        ave_range_mm = sum(range) / 4

        return ave_range_mm / 10  # Return cm

    def _write(self, msg: bytes):
        print(self._uart.write(msg))

    def _read(self) -> str | None:
        self._uart.flush()
        sleep_ms(500)
        value = self._uart.readline()
        # print(f"{value=}")
        if value:
            return value.decode("utf-8")
        return None
