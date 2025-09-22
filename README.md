# kid_car_horn
RP2040 software to implement kid's car horn

# What do will need?

The following tools were used during development of this project:
1. PyCharm
2. [MicroPython Tools](https://plugins.jetbrains.com/plugin/26227-micropython-tools)
3. [Sox](https://formulae.brew.sh/formula/sox) is used to convert common audio files to raw binary files
4. [Audacity](https://www.audacityteam.org/download/mac/) if you want to edit audio files

# Hardware

1. RP2040 micro board from AliExpress
2. A tiny sound speaker and an amplifier
3. 3.7V battery
4. Charge controller
5. A switch with keys
6. Toy car (modifying the steering wheel), 3 buttons and 2 leds are included


# Something use

Convert wav/mp3 on your Mac:
```sox data/source/honk-middle-shor.wav -r 8000 -c 1 -b 8 -e unsigned-integer mcu/data/out.raw```
