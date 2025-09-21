import time

from machine import Pin, PWM

# Setup buzzer on GPIO 25
buzzer = PWM(Pin(0))

DUTY = 10000

# 🎵 Note frequencies (C3–B5 + R for rest)
NOTES = {
    # Octave 3
    'C3': 130, 'C#3': 138, 'Db3': 138, 'D3': 146, 'D#3': 155, 'Eb3': 155, 'E3': 164,
    'F3': 174, 'F#3': 185, 'Gb3': 185, 'G3': 196, 'G#3': 207, 'Ab3': 207, 'A3': 220,
    'A#3': 233, 'Bb3': 233, 'B3': 246,

    # Octave 4
    'C4': 261, 'C#4': 277, 'Db4': 277, 'D4': 293, 'D#4': 311, 'Eb4': 311, 'E4': 329,
    'F4': 349, 'F#4': 370, 'Gb4': 370, 'G4': 392, 'G#4': 415, 'Ab4': 415, 'A4': 440,
    'A#4': 466, 'Bb4': 466, 'B4': 493,

    # Octave 5
    'C5': 523, 'C#5': 554, 'Db5': 554, 'D5': 587, 'D#5': 622, 'Eb5': 622, 'E5': 659,
    'F5': 698, 'F#5': 740, 'Gb5': 740, 'G5': 784, 'G#5': 831, 'Ab5': 831, 'A5': 880,
    'A#5': 932, 'Bb5': 932, 'B5': 987,

    # Rest
    'R': 0
}

# 🎵 Duration symbols to beat ratios
DURATIONS = {
    'W': 4.0,  # Whole
    'H': 2.0,  # Half
    'Q': 1.0,  # Quarter
    'E': 0.5,  # Eighth
    'S': 0.25,  # Sixteenth
    'QE': 1.5,  # Dotted quarter
    'HQ': 3.0,  # Dotted half
}


# 🧮 Convert symbol to seconds using BPM
def duration_to_seconds(symbol, bpm):
    beats = DURATIONS.get(symbol.upper(), 1.0)
    return (60.0 / bpm) * beats


# 🔊 Play a single note
def play_tone(freq, duration):
    print(f"Playing {freq} Hz for {duration:.2f} s")
    if freq == 0:
        buzzer.duty_u16(0)
    else:
        buzzer.freq(freq)
        buzzer.duty_u16(DUTY)
    time.sleep(duration)
    buzzer.duty_u16(0)
    time.sleep(0.05)


# 📄 Parse "NOTE-DURATION" string into list
def parse_melody_string(melody_str):
    parts = melody_str.strip().split()
    result = []
    for part in parts:
        if '-' not in part:
            continue
        note, dur = part.split('-')
        result.append((note.strip().upper(), dur.strip().upper()))
    return result

melody = """
E5-H   D5-H   B4-H   D5-Q  E5-Q
E5-H   D5-H   B4-H   D5-Q  E5-Q
G5-H   F#5-Q  E5-Q  D5-H
E5-H   D5-H   B4-H   D5-Q  E5-Q"""


# ▶️ Play a melody string
def play_melody_string(melody_str, bpm=120):
    sequence = parse_melody_string(melody_str)
    for note_name, dur_symbol in sequence:
        freq = NOTES.get(note_name, 0)
        duration = duration_to_seconds(dur_symbol, bpm)
        play_tone(freq, duration)
