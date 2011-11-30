# -*- coding: iso-8859-15 -*-
import subprocess, fcntl, os, select, sys, re, time
import gtk, gobject, datetime
import log

from settings import *

gobject.threads_init()

def burn(button, filename):
	global GBLprocess
	global GBLline
	global GBLoutput
	global GBLtimeStartedBurn
	
	log.logMessage("BeginDiscWrite", "'" + filename + "'", "")
	
	showProgressWindow()
	
	# close the 'ready to burn' window
	parentWindow = button.get_parent_window()
	parentWindow.destroy()
	
	command = KA_Program, 'dev=' + KA_Device, '-tao', 'gracetime=0', '-v', '-eject', filename
	
	GBLprocess = subprocess.Popen(command, 0, KA_Program, subprocess.PIPE, 
							   subprocess.PIPE, subprocess.STDOUT)
	
	flags = fcntl.fcntl(GBLprocess.stdout, fcntl.F_GETFL)
	fcntl.fcntl(GBLprocess.stdout, fcntl.F_SETFL, flags | os.O_NONBLOCK)
	
	GBLline = ''
	GBLoutput = []
	GBLtimeStartedBurn = datetime.datetime.now()
	
	# have gtk call updateProgress every quarter of a second
	gobject.timeout_add(250, updateProgress)
	
# rc is the return code from wodim
def burnFinished(rc):
	global progressWindow
	global caughtErr
	
	window = gtk.Window(gtk.WINDOW_TOPLEVEL)
	window.set_default_size(KA_ScreenResolution[0], KA_ScreenResolution[1])
	#window.set_title("burn.py - WLFT-KA")
	window.set_title("IdatuxFT")
	window.fullscreen()
	
	if rc == 0:
		title = "Grabación completa!"
		desc = "Tu disco está listo para que lo uses!."
		img = "yes"
		log.logMessage("DiskWriteSuccess", "", "")
	else:
		title = "La grabación ha fallado."
		desc = "Tu disco no pudo ser grabado."
		img = "no"
		log.logMessage("DiskWriteFailue", "", "")
		

	titleLabel = gtk.Label("<span size='36000'><b>" + title + "</b></span>")
	titleLabel.set_justify(gtk.JUSTIFY_CENTER)
	titleLabel.set_selectable(False)
	titleLabel.set_use_markup(True)
	
	image = gtk.Image()
	image.set_from_file(KA_UIDir + "done." + img + ".png")
	
	descLabel = gtk.Label("<span size='14000'>" + desc + "</span>")
	descLabel.set_justify(gtk.JUSTIFY_CENTER)
	descLabel.set_line_wrap(True)
	descLabel.set_selectable(False)
	descLabel.set_use_markup(True)
	
	exit = gtk.Button()
	exit.set_focus_on_click(False)
	exit.connect("clicked", closeWindowAndEjectCbk, window)
	
	icon = gtk.Image()
	icon.set_from_file(KA_UIDir + 'details.back.png')
	label = gtk.Label("<span size='24000'>Menú principal</span>")
	label.set_use_markup(True)
	
	exitlayout = gtk.HBox(False, 10)
	
	exitlayout.pack_start(icon, False, False)
	exitlayout.pack_start(label, True, True)
	exit.add(exitlayout)
	
	vbox = gtk.VBox(False, 10)
	vbox.pack_start(titleLabel, True, False)
	vbox.pack_start(image, True, False)
	vbox.pack_start(descLabel, True, False)
	vbox.pack_start(exit, False, False)
	
	window.add(vbox)
	window.show_all()

	closeWindowAndEject(progressWindow)
	
	# close window after timeout passes
	gobject.timeout_add(KA_WindowTimeout, window.destroy)

def closeWindowAndEject(window):
	window.destroy()
	
def closeWindowAndEjectCbk(button, window):
	closeWindowAndEject(window)
	
def eject():
	os.system("eject " + KA_Device)

def showProgressWindow():
	global progressWindow
	global timeLeftLbl
	global timeLeftIcon
	global percentComplete
	
	progressWindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
	progressWindow.set_default_size(KA_ScreenResolution[0], KA_ScreenResolution[1])
	progressWindow.fullscreen()
	
	title = gtk.Label("<span size='40000'><b>grabando...</b></span>")
	title.set_use_markup(True)
	title.set_selectable(False)
	title.set_justify(gtk.JUSTIFY_CENTER)
	
	timeLeftIcon = gtk.Image()
	timeLeftIcon.set_from_file(KA_UIDir + 'progress.00.png')
	
	timeLeftTitle = gtk.Label("<span size='20000'><b>Tiempo restante:</b></span>")
	timeLeftTitle.set_use_markup(True)
	timeLeftTitle.set_selectable(False)
	timeLeftTitle.set_justify(gtk.JUSTIFY_CENTER)
	
	progressBar = gtk.ProgressBar()
	progressBar.set_pulse_step(0.1)
	progressBar.pulse()
	
	timeLeftLbl = gtk.Label("<span size='24000'>4 a 6 minutos</span>")
	timeLeftLbl.set_use_markup(True)
	timeLeftLbl.set_selectable(False)
	timeLeftLbl.set_justify(gtk.JUSTIFY_CENTER)
	
	percentComplete = gtk.Label("<span size='14000'></span>")
	percentComplete.set_use_markup(True)
	percentComplete.set_selectable(False)
	percentComplete.set_justify(gtk.JUSTIFY_CENTER)
	
	layout = gtk.VBox()
	layout.pack_start(title, True, True)
	layout.pack_start(timeLeftIcon, True, True)
	layout.pack_start(timeLeftTitle, True, True)
	layout.pack_start(timeLeftLbl, True, True)
	# layout.pack_start(percentComplete, True, True) Used for debugging. You can enable it if you want
	progressWindow.add(layout)
	progressWindow.show_all()
	
def updateProgress():
	global GBLprocess
	global GBLline
	global GBLoutput
	
	haveData = True
	while haveData:
		# Check if any data is available from the pipe.
		[i, o, e] = select.select([GBLprocess.stdout], [], [], 0.1)
		if i:
			char = GBLprocess.stdout.read(1)
			
			if char == '':
				if GBLprocess.poll() is None:
					# process is still running, wait until it dies
					time.sleep(1)
					continue
				else:
					burnFinished(GBLprocess.poll())
					return False
				
			if char == '\r':
				# replace carriage return with newline
				char = '\n'
			
			if not char == '\b':
				# ignore backspace
				GBLline += char
			
			if char == '\n':
				#sys.stdout.write(GBLline)
				log.logWodim(GBLline)
				
				# save the GBLline
				GBLoutput.append(GBLline)
				
				# check if this is a progress line
				if re.match('^Track', GBLline):
					estimateTimeLeft(GBLline)
				
				GBLline = ''
				
				if re.compile("Re-load disk and hit <CR>").match(GBLoutput[-1]):
					# wodim is asking me to press enter
					GBLprocess.stdin.write("\n")
		else:
			haveData = False
	
	# poll() will return the process's return code if it dies
	# or None if it's still running.
	if not GBLprocess.poll() is None:
		burnFinished(GBLprocess.poll())
		return False
	
	return True

def estimateTimeLeft(line):
	global timeLeftLbl
	global timeLeftIcon
	global percentComplete
	global GBLtimeStartedBurn
	
	# line looks like 'Track 01:   92 of  120 MB written (fifo  98%) [buf  92%]   4.2x.\n'
	megsWritten = re.findall('\s+(\d+) of', line)
	
	# line not in proper format
	if len(megsWritten) == 0 or int(megsWritten[0]) == 0:
		return
	
	# won't get a good time estimate until wrote at least 30 M, but still update percent label
	if int(megsWritten[0]) < 30:
		return
	
	timeNow = datetime.datetime.now()
	
	# can't calculate speed
	if timeNow == GBLtimeStartedBurn:
		return
	
	totalMegs = re.findall(' of\s+(\d+)', line)
	
	written = round(float(megsWritten[0]), 1)
	total = round(float(totalMegs[0]), 1)
	
	# line not in proper format
	if len(totalMegs) == 0:
		return
	
	timeLeft = (timeNow - GBLtimeStartedBurn).seconds * (int(totalMegs[0]) - int(megsWritten[0])) / \
			   int(megsWritten[0])
	
	# 30 seconds for fixating and such
	timeLeft += 30
	
	percent = (written / total) * 100
	
	percentComplete.set_text("<span size='14000'>" + str(round(percent, 1)) + "%</span>")
	percentComplete.set_use_markup(True)

	# display a visual progress bar using percent calculated by dividing amount burned by filesize
	if percent == 100:
		timeLeftIcon.set_from_file(KA_UIDir + 'progress.100.png')
	elif percent >= 90:
		timeLeftIcon.set_from_file(KA_UIDir + 'progress.90.png')
	elif percent >= 80:
		timeLeftIcon.set_from_file(KA_UIDir + 'progress.80.png')
	elif percent >= 70:
		timeLeftIcon.set_from_file(KA_UIDir + 'progress.70.png')
	elif percent >= 60:
		timeLeftIcon.set_from_file(KA_UIDir + 'progress.60.png')
	elif percent >= 50:
		timeLeftIcon.set_from_file(KA_UIDir + 'progress.50.png')
	elif percent >= 40:
		timeLeftIcon.set_from_file(KA_UIDir + 'progress.40.png')
	elif percent >= 30:
		timeLeftIcon.set_from_file(KA_UIDir + 'progress.30.png')
	elif percent >= 20:
		timeLeftIcon.set_from_file(KA_UIDir + 'progress.20.png')
	elif percent >= 10:
		timeLeftIcon.set_from_file(KA_UIDir + 'progress.10.png')
	else:
		timeLeftIcon.set_from_file(KA_UIDir + 'progress.00.png')
	
	if timeLeft / 60 + 1 > 1:
		timeLeftLbl.set_text("<span size='24000'>" + str(timeLeft / 60 + 1) + " minutes</span>")
	elif timeLeft == 30:
		timeLeftLbl.set_text("<span size='24000'>Terminando...</span>")
	else:
		timeLeftLbl.set_text("<span size='24000'>1 minuto</span>")

	timeLeftLbl.set_use_markup(True)
