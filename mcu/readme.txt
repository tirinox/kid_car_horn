# Example usage:
# Convert on your Mac:
#   sox input.wav -r 8000 -c 1 -b 8 -e unsigned-integer out.raw
# Upload:
#   mpremote cp out.raw :out.raw
# Play:
#   play_raw_pwm("out.raw", sample_rate=8000, carrier_hz=32000)
