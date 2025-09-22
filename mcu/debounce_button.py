import time

from machine import Pin


class DebouncedButton:
    def __init__(self, pin: Pin, debounce_ms: int = 50, active_level: int = 0):
        self._pin = pin
        self._debounce_ms = debounce_ms
        self._active_level = active_level

        self._last_state = self._pin.value()
        self._stable_state = self._last_state
        self._last_change_time = time.ticks_ms()

        self._pressed_event = False
        self._released_event = False

    def update(self):
        now = time.ticks_ms()
        cur = self._pin.value()

        if cur != self._last_state:
            self._last_state = cur
            self._last_change_time = now

        elif cur != self._stable_state:
            if time.ticks_diff(now, self._last_change_time) >= self._debounce_ms:
                self._stable_state = cur
                if self._stable_state == self._active_level:
                    self._pressed_event = True
                else:
                    self._released_event = True

    def pressed(self) -> bool:
        if self._pressed_event:
            self._pressed_event = False
            return True
        return False

    def released(self) -> bool:
        if self._released_event:
            self._released_event = False
            return True
        return False

    def is_pressed(self) -> bool:
        return self._stable_state == self._active_level
