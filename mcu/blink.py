import time

import machine
import neopixel


def blink_led():
    # Pin 16, 1 pixel
    pin = machine.Pin(16, machine.Pin.OUT)
    np = neopixel.NeoPixel(pin, 1)

    while True:
        # Turn ON (red)
        np[0] = (100, 0, 0)  # (R, G, B)
        np.write()
        time.sleep(0.5)

        # Turn OFF
        np[0] = (0, 100, 0)
        np.write()
        time.sleep(0.5)
