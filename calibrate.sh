#!/bin/bash

# Re-invert the axis so they're going the right way
xinput set-int-prop \
"Elo TouchSystems, Inc. Elo TouchSystems IntelliTouch 2500U" \
"Evdev Axis Inversion" 8 1 1
# ^^ format: 8 (don't modify), (flip X), (flip Y) [1/0 = true/false]

# Recalibrate the touchscreen (tested, it's spot-on)
xinput set-int-prop \
"Elo TouchSystems, Inc. Elo TouchSystems IntelliTouch 2500U" \
"Evdev Axis Calibration" 32 0 4096 0 4096
# ^^ format: 32 (don't modify), (min X), (max X), (min Y), (max Y) [integers]
