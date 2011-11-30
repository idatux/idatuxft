#!/bin/bash

# If you changed the log name in settings.py or here, change it there/here too
LOGFILENAME=logs/active.txt

LOGARCHIVEDNAME="logs/log-`date +'%Y-%m-%d'`.tar.gz"

if [ ! -e $LOGFILENAME ]; then
	echo "Log file could not be found."
	zenity --error --text="Log file could not be found." --timeout=5
	exit
fi

tar -czf "${LOGARCHIVEDNAME}" "${LOGFILENAME}"
echo > $LOGFILENAME

echo "${LOGFILENAME} -> ${LOGARCHIVEDNAME}"
zenity --info --text="Log successfully archived as ${LOGARCHIVEDNAME}" --timeout=5
