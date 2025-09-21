import machine

from wavplay import play_raw_pwm, play_cached_pwm

# pin 1 = button
#
button_pin = machine.Pin(1, machine.Pin.IN, machine.Pin.PULL_UP)


def honk_start():
    play_cached_pwm("data/honk-start.raw", 8000)


def honk_middle():
    play_cached_pwm("data/honk-middle-short.raw", 8000)


def honk_end():
    play_cached_pwm("data/honk-end.raw", 8000)


def honk():
    honk_start()
    honk_middle()
    honk_middle()
    honk_end()


def main():
    is_honking = False
    while True:
        if button_pin.value() == 0:  # button pressed
            if not is_honking:
                is_honking = True
                honk_start()
            else:
                honk_middle()
        else:
            if is_honking:
                is_honking = False
                honk_end()
            machine.lightsleep(100)
        # beep_example()


if __name__ == '__main__':
    main()
