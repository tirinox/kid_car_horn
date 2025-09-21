# Passive buzzer on pin 0
import time

import machine

buzzer = machine.PWM(machine.Pin(0))


def beep(freq=1000, duration=500):
    """
    Play a tone on the buzzer
    freq = frequency in Hz
    duration = time in milliseconds
    """
    buzzer.freq(freq)
    buzzer.duty_u16(10000)
    time.sleep_ms(duration)
    buzzer.duty_u16(0)  # turn off


def beep_example():
    """
    Example usage: play a tone and a melody
    """
    # Example: play a 1kHz tone for 0.5 seconds
    # beep(1000, 500)

    # Example: play a small melody
    for f in [523, 587, 659, 698, 784]:  # C D E F G
        beep(f, 100)
        time.sleep_ms(10)
