<!-- SPDX-License-Identifier: MIT -->
<!-- SPDX-FileCopyrightText: Copyright 2025 Sam Blenny -->
# Synthio Click Reproducer (BCLK Improvements)

This one is aimed at getting the BCLK PLL input option working as well as
possible. Basically, what I've learned here is that even if I carefully follow
all the guidance in the datasheet for configuration sequencing and PLL register
values, the PLL still won't lock from BCLK.

When the PLL doesn't lock, you get lots of harmonic distortion, particularly
for lower sample rates. There's also broadband noise extending above the
Nyquist frequency. The noise can be mitigated substantially by balancing the
`dac_volume` (digital) and `headphone_volume` (analog) volume settings. For a
BCLK line level output, `dac_volume = -3` and `headphone_volume = 0` sounds
relatively good (lower noise floor but still suffers from harmonic distortion).

My conclusion is that using MCLK sounds much better than relying on BCLK, and
there don't seem to be any further options for improving BCLK as a PLL input.
