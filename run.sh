#!/bin/bash

# Note: run.sh is intended to be used to run the kiosk application in its own
# X server, and not while one is already running. If you wish to do run it
# in an already running X server, use 'python main.py' to avoid conflicts.

SOFTWAREDIR=/home/alex/Desktop/wlhs-ka/
cd ${SOFTWAREDIR}

if [ -e ./engine/main.py ]; then
	cd engine
	X :1 -ac & DISPLAY=:1 ./main.py
else
	echo "Aborting: main menu file could not be found."
fi
