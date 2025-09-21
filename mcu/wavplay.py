# pwm_raw_player.py  — ESP32 + MicroPython
# Plays unsigned 8-bit mono RAW at SAMPLE_RATE via high-frequency PWM

import time

from machine import Pin, PWM

# === Settings ===
BUZZER_PIN = 0  # your buzzer GPIO
CARRIER_HZ = 64000  # PWM carrier (ultrasonic-ish)
DEFAULT_SR = 8000  # audio sample rate of your RAW file
CHUNK_BYTES = 4096  # I/O buffer size

# Create PWM once
_pwm = PWM(Pin(BUZZER_PIN), freq=CARRIER_HZ)
# Try to detect duty API
_HAS_U16 = hasattr(_PWM := _pwm, "duty_u16")

# Precompute 0..255 -> duty
if _HAS_U16:
    # 16-bit duty range
    _LUT = bytearray(256 * 2)  # not used directly, but keep placeholder


    def _duty_from_u8(x):
        return (x << 8) | x  # 0..65535 (scale 0..255 to 0..65535)
else:
    # Classic ESP32 PWM: 0..1023
    def _duty_from_u8(x):
        return (x * 1023) // 255


def _set_duty(val):
    if _HAS_U16:
        _PWM.duty_u16(val)
    else:
        _PWM.duty(val)


# Module-level cache: filename -> {"data": memoryview, "frames": int, "path": str}
AUDIO_CACHE = {}


def preload_raw_pwm(path):
    """
    Ensure 'path' is preloaded into AUDIO_CACHE and return the cache record.
    Loads from disk only on first use.
    """
    rec = AUDIO_CACHE.get(path)
    if rec is not None:
        return rec

    with open(path, "rb") as f:
        data = f.read()

    rec = {
        "data": memoryview(data),  # zero-copy iteration
        "frames": len(data),
        "path": path,
    }
    AUDIO_CACHE[path] = rec
    return rec


def play_preloaded_pwm(preloaded, sample_rate=DEFAULT_SR, carrier_hz=CARRIER_HZ):
    """
    Play preloaded raw 8-bit unsigned mono PCM via PWM.
    """
    _PWM.freq(carrier_hz)
    _set_duty(0)

    period_us = int(1_000_000 // sample_rate)

    try:
        t0 = time.ticks_us()
        frames_played = 0
        data = preloaded["data"]

        for sample in data:  # 0..255
            _set_duty(_duty_from_u8(sample))
            frames_played += 1
            target = t0 + frames_played * period_us
            while time.ticks_diff(target, time.ticks_us()) > 0:
                pass
    finally:
        _set_duty(0)


def play_cached_pwm(path, sample_rate=DEFAULT_SR, carrier_hz=CARRIER_HZ):
    """
    Convenience: preload (from cache or disk) and play.
    """
    rec = preload_raw_pwm(path)
    play_preloaded_pwm(rec, sample_rate=sample_rate, carrier_hz=carrier_hz)


def play_raw_pwm(path, sample_rate=DEFAULT_SR, carrier_hz=CARRIER_HZ):
    # (Re)configure carrier in case caller changed it
    _PWM.freq(carrier_hz)
    _set_duty(0)

    # Timing
    period_us = int(1_000_000 // sample_rate)

    # Stream in chunks to avoid RAM blowups
    buf = bytearray(CHUNK_BYTES)

    try:
        with open(path, "rb") as f:
            # Optional: quick sanity print
            # print("Size:", os.stat(path)[6], "bytes")

            t0 = time.ticks_us()
            frames_played = 0

            while True:
                n = f.readinto(buf)
                if not n:
                    break

                # Tight playback loop
                for i in range(n):
                    sample = buf[i]  # 0..255 unsigned
                    _set_duty(_duty_from_u8(sample))
                    frames_played += 1

                    # pace to sample rate
                    target = t0 + frames_played * period_us
                    while time.ticks_diff(target, time.ticks_us()) > 0:
                        pass
    finally:
        _set_duty(0)

# Example usage:
# Convert on your Mac:
#   sox input.wav -r 8000 -c 1 -b 8 -e unsigned-integer out.raw
# Upload:
#   mpremote cp out.raw :out.raw
# Play:
#   play_raw_pwm("out.raw", sample_rate=8000, carrier_hz=32000)
