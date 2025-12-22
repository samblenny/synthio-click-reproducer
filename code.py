# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: Copyright 2025 Sam Blenny
#
# WAV file beep demo for Fruit Jam (adjust pins as needed for other boards)
#
from audiobusio import I2SOut
import audiocore
from board import (
    I2C, I2S_BCLK, I2S_DIN, I2S_MCLK, I2S_WS, PERIPH_RESET
)
from digitalio import DigitalInOut, Direction, Pull
from pwmio import PWMOut
import time
from adafruit_tlv320 import TLV320DAC3100

# To try different sample rates, change which one of these is uncommented
#SAMPLE_RATE = 48000
#SAMPLE_RATE = 44100
#SAMPLE_RATE = 22050
#SAMPLE_RATE = 11025
SAMPLE_RATE = 8000

BUFFER_SIZE = 512

# Reset Fruit Jam rev D TLV320 I2S DAC
rst = DigitalInOut(PERIPH_RESET)
rst.direction = Direction.OUTPUT
rst.value = False
time.sleep(0.1)
rst.value = True
time.sleep(0.05)

# Configure DAC (NOTE: The 5 MHz PWMOut to I2S_MCLK is essential!)
i2c = I2C()
dac = TLV320DAC3100(i2c)
mclk_out = PWMOut(I2S_MCLK, frequency=5_000_000, duty_cycle=2**15)
dac.configure_clocks(sample_rate=SAMPLE_RATE, bit_depth=16, mclk_freq=5_000_000)
dac.speaker_output = False
dac.headphone_output = True
dac.headphone_volume = -6    # CAUTION! Line level. Too loud for headphones!
audio = I2SOut(bit_clock=I2S_BCLK, word_select=I2S_WS, data=I2S_DIN)

# Load wav file with 650 Hz beep at the specified sample rate
sample = audiocore.WaveFile({
    8000: "sinewave_8kHz.wav",
    11025: "sinewave_11kHz.wav",
    22050: "sinewave_22kHz.wav",
    44100: "sinewave_44kHz.wav",
    48000: "sinewave_48kHz.wav",
}[SAMPLE_RATE])

# Send wav file beeps on the Fruit Jam DAC
print(f"Beeping at sample rate {SAMPLE_RATE} Hz...")
time.sleep(0.5)
while True:
    audio.play(sample)
    time.sleep(2)
