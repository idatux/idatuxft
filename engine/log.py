import datetime
from settings import *

def logMessage(messageName, isoFilename, isoName):
	timeNow = datetime.datetime.now()
	timeNow = str(timeNow.year) + '-' + str(timeNow.month) + '-' + str(timeNow.day) + ' ' +\
			str(timeNow.hour) + ':' + str(timeNow.minute) + ':' + str(timeNow.second)

	logFile = open(KA_LogFile, "a")
	logFile.write(timeNow + '\t' + messageName + '\t' + isoFilename + '\t' + isoName + '\n')
	
	print timeNow + '\t' + messageName + '\t' + isoFilename + '\t' + isoName

def logWodim(message):
	timeNow = datetime.datetime.now()
	timeNow = str(timeNow.year) + '-' + str(timeNow.month) + '-' + str(timeNow.day) + '/' +\
			str(timeNow.hour) + ':' + str(timeNow.minute) + ':' + str(timeNow.second)

	logFile = open(KA_LogFile, "a")
	logFile.write(timeNow + '\t' + KA_Program + '\t' + message)
	
	print timeNow + '\t' + KA_Program + '\t' + message

