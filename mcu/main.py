import time

import machine
from machine import Pin

from mcu.debounce_button import DebouncedButton
from wavplay import play_cached_pwm


class Horn:
    def __init__(self, pin: Pin):
        self._pin = pin
        self._is_honking = False

    @staticmethod
    def honk_start():
        play_cached_pwm("data/honk-start.raw")

    @staticmethod
    def honk_middle():
        play_cached_pwm("data/honk-middle-short.raw")

    @staticmethod
    def honk_end():
        play_cached_pwm("data/honk-end.raw", )

    def handle(self):
        if self._pin.value() == 0:  # button pressed
            if not self._is_honking:
                self._is_honking = True
                self.honk_start()
            else:
                self.honk_middle()
            return True
        else:
            if self._is_honking:
                self._is_honking = False
                self.honk_end()
            return False

    def full_honk(self):
        self.honk_start()
        self.honk_middle()
        self.honk_end()


class TurnSignal:
    def __init__(self, button: DebouncedButton, out: Pin, period_ms=1000):
        self._button = button
        self._out = out
        self._period_ms = period_ms
        self._last_triggered_time = 0
        self._is_tick = True
        self._is_active = False

    TICK_SOUND = 'data/turn-signal-tick.wav'
    TOCK_SOUND = 'data/turn-signal-tick.wav'

    def play_tick_tock(self):
        play_cached_pwm(self.TICK_SOUND if self._is_tick else self.TOCK_SOUND)
        self._is_tick = not self._is_tick
        self._last_triggered_time = time.ticks_ms()

    def toggle_active(self):
        self._is_active = not self._is_active

        if self._is_active:
            self.play_tick_tock()
            self._out.value(1)
        else:
            self._out.value(0)

    def handle(self):
        """
        Returns true if active
        Do not call long sleeps
        Do tick-tock every _period_ms
        """
        # if button is pressed
        self._button.update()
        if self._button.is_pressed():
            self.toggle_active()

        if self._is_active:
            now = time.ticks_ms()
            if time.ticks_diff(now, self._last_triggered_time) >= self._period_ms:
                self.play_tick_tock()
                # мигнём выходом
                self._out.value(0 if self._out.value() else 1)

        return self._is_active


def main():
    pin_left = Pin(1, Pin.IN, Pin.PULL_UP)
    pin_middle = Pin(2, Pin.IN, Pin.PULL_UP)
    pin_right = Pin(3, Pin.IN, Pin.PULL_UP)

    button_left = DebouncedButton(pin_left, debounce_ms=50)
    button_right = DebouncedButton(pin_right, debounce_ms=50)
    led_left = Pin(4, Pin.OUT)
    led_right = Pin(5, Pin.OUT)
    left_signal = TurnSignal(button_left, led_left)
    right_signal = TurnSignal(button_right, led_right)

    horn = Horn(pin_middle)

    while True:
        horn_active = horn.handle()
        left_active = left_signal.handle()
        right_active = right_signal.handle()
        if not (horn_active or left_active or right_active):
            machine.lightsleep(20)


if __name__ == '__main__':
    main()
