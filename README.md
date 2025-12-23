<!-- SPDX-License-Identifier: MIT -->
<!-- SPDX-FileCopyrightText: Copyright 2025 Sam Blenny -->
# Synthio Click Reproducer (BCLK vs Sample Rate)

Logic analyzer measurements of I2S BCLK Hz vs DAC sample rate for Fruit Jam.


## Saleae + Fruit Jam wiring:

| Pin | I2S Signal |
| --- | ---------- |
| A2  | BCLK |
| A3  | WSEL |
| A4  | DIN  |


## Summary of BCLK Frequencies

| Sample Rate | mean BCLK   | sample rate * 32 |
| ----------- | ----------- | ---------------- |
| 8000        | 256.011 kHz |  256000          |
| 11025       | 352.797 kHz |  352800          |
| 22050       | 705.529 kHz |  705600          |
| 44100       | 1.411 MHz   | 1411200          |
| 48000       | 1.535 MHz   | 1536000          |


## BCLK for 8000 Hz Sample Rate

![BCLK_8000.png](BCLK_8000.png)


## BCLK for 11025 Hz Sample Rate

![BCLK_11025.png](BCLK_11025.png)


## BCLK for 22050 Hz Sample Rate

![BCLK_22050.png](BCLK_22050.png)


## BCLK for 44100 Hz Sample Rate

![BCLK_44100.png](BCLK_44100.png)


## BCLK for 48000 Hz Sample Rate

![BCLK_48000.png](BCLK_48000.png)
