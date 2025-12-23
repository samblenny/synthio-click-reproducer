# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: Copyright 2025 Sam Blenny
#
# WAV file beep demo for Fruit Jam (adjust pins as needed for other boards)
#
import time

import audiocore
from audiobusio import I2SOut
from board import I2C, I2S_BCLK, I2S_DIN, I2S_MCLK, I2S_WS, PERIPH_RESET
from digitalio import DigitalInOut, Direction, Pull
from micropython import const
from pwmio import PWMOut

from adafruit_tlv320 import TLV320DAC3100

# I2S MCLK clock frequency
MCLK_HZ = const(15_000_000)


def configure_dac(i2c, sample_rate, reset_pin):
    # Configure TLV320DAC
    # NOTE: You must provide a 15 MHz PWMOut clock to the DAC's MCLK pin!
    # 1. Hard reset
    rst = DigitalInOut(reset_pin)
    rst.direction = Direction.OUTPUT
    rst.value = False
    time.sleep(0.05)
    rst.value = True
    time.sleep(0.05)
    rst.deinit()
    # 2. Configure clock, signal routing, and volume settings
    dac = TLV320DAC3100(i2c)
    dac.configure_clocks(sample_rate=sample_rate, bit_depth=16, mclk_freq=MCLK_HZ)
    dac.speaker_output = False
    dac.headphone_output = True
    dac.headphone_volume = -6  # CAUTION! Line level. Too loud for headphones!
    # 3. Wait for amp to power up and volume to stabilize
    time.sleep(0.4)
    return dac


# Set up I2C and I2S buses
i2c = I2C()
audio = I2SOut(bit_clock=I2S_BCLK, word_select=I2S_WS, data=I2S_DIN)

# Set up 15 MHz MCLK PWM clock output (this stops audio hiss)
mclk_pwm = PWMOut(I2S_MCLK, frequency=MCLK_HZ, duty_cycle=2**15)

# Loop through all the sample rates
sample_rates = (
    (8000, "sinewave_8kHz.wav", 2),  # 8000 gets 2 beeps
    (11025, "sinewave_11kHz.wav", 3),  # 11025 gets 3 beeps
    (22050, "sinewave_22kHz.wav", 4),  # 4 beeps
    (44100, "sinewave_44kHz.wav", 5),  # ...
    (48000, "sinewave_48kHz.wav", 6),
)
while True:
    for sample_rate, filename, beeps in sample_rates:
        # Reset and re-configure DAC for the current sample rate
        dac = configure_dac(i2c, sample_rate, reset_pin=PERIPH_RESET)

        # Load wav file with 650 Hz beep at this sample rate
        sample = audiocore.WaveFile(filename)

        # Play beeps
        print(f"Beeping {beeps} times at sample rate {sample_rate} Hz...")
        for _ in range(beeps):
            audio.play(sample)
            time.sleep(0.35)

        # Pause before next sample rate
        time.sleep(0.8)

    # Pause before starting over
    print()
    time.sleep(3)
