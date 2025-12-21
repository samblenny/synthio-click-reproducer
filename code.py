# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: Copyright 2025 Sam Blenny
from audiobusio import I2SOut
import audiocore
from board import (
    I2C, I2S_BCLK, I2S_DIN, I2S_MCLK, I2S_WS, PERIPH_RESET
)
from digitalio import DigitalInOut, Direction, Pull
import synthio
import time
import ulab.numpy as np
from adafruit_tlv320 import TLV320DAC3100


#SAMPLE_RATE = 48000   # Sounds okay (maybe some slight filter ringing/phasing?)
#SAMPLE_RATE = 44100  # Sounds pretty good
#SAMPLE_RATE = 22050  # Note: lots of harmonics and aliasing
#SAMPLE_RATE = 11025  # Even more harmonics and aliasing
SAMPLE_RATE = 8000
BUFFER_SIZE = 64

# Reset Fruit Jam rev D TLV320 I2S DAC
rst = DigitalInOut(PERIPH_RESET)
rst.direction = Direction.OUTPUT
rst.value = False
time.sleep(0.1)
rst.value = True
time.sleep(0.05)

# Configure DAC
i2c = I2C()
dac = TLV320DAC3100(i2c)
dac.configure_clocks(sample_rate=SAMPLE_RATE, bit_depth=16)
dac.speaker_output = False
dac.headphone_output = True
dac.headphone_volume = -6    # CAUTION! Line level. Too loud for headphones!
audio = I2SOut(bit_clock=I2S_BCLK, word_select=I2S_WS, data=I2S_DIN)

# Load 12 WPM wav files (100ms dit, 300ms dah)
dit = audiocore.WaveFile("dit_8kHz_12wpm.wav")
dah = audiocore.WaveFile("dah_8kHz_12wpm.wav")

# Send Morse code ("C") with synthio sinewave notes on the Fruit Jam DAC
time.sleep(0.5)
note = synthio.Note(frequency=650)
while True:
    for (sample, s) in ((dah, 0.3), (dit, 0.1), (dah, 0.3), (dit, 0.1)):
        audio.play(sample)
        time.sleep(s + 0.1)
    time.sleep(2)
