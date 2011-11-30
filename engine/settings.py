# Settings File
# 
# This is the main settings file for the wlhs-ka engine.
# Don't change the names of any variables unless you feel like changing them
# where they are referenced too.
#
# --------------------
#
# Settings Documentation:
#
# KA_Name
# string
# The text that appears on the main menu to serve as the title.
#
# KA_ScreenResolution
# list [integer, integer]
# The screen resolution of the monitor the software will run on.
#
# KA_BaseDir
# string
# The base directory where the software folder 'lives'.
#
# ISO_EnabledDir
# string
# Where the (symbolic-linked) ISO and description files are that will be
# displayed on the main menu screen.
#
# ISO_AvailDir
# string
# Where all of the available ISO and description files are.
#
# ISO_ImagePath
# string
# Where the images for the buttons are.
#
# ISO_MaxNumber
# integer
# The maximum number of ISO files to load before stopping.
#
# KA_AboutFile
# string
# The file to load when the "About" button in the main menu is pressed.
#
# KA_AuthorsFile
# string
# The file to load when the "Authors" button in the main menu is pressed.
#
# KA_HelpFile
# string
# The file to load when the "Help" button in the main menu is pressed.
#
# KA_WindowTimeout
# integer
# The time after which a screen that isn't the main menu or burn progress screen
# will close. Time is in milliseconds.
#
# KA_Program
# string
# The program to use to burn the discs.
#
# KA_Device
# string
# The device to use to burn the discs.
#
# KA_LogFile
# string
# The log file to write to.
#
# --------------------								Legacy equivalent:

KA_Name = "Idatux Freedom Toaster"
KA_ScreenResolution = 1024, 600				# RESOLUTION
KA_BaseDir = "/opt/IdatuxFT/"

ISO_EnabledDir = KA_BaseDir + "content-enabled/"	# ISOLISTDIR
ISO_AvailDir = KA_BaseDir + "content-available/"	# ISOPATH
ISO_ImagePath = ISO_AvailDir + "imgs/"			# ISOIMAGEPATH
ISO_MaxNumber = 8					# MAXISOS

KA_AboutFile = KA_BaseDir + "elproyecto.html"
KA_AuthorsFile = KA_BaseDir + "idatux.html"
KA_HelpFile = KA_BaseDir + "ayuda.html"			# HELPFILE
KA_UIDir = KA_BaseDir + "engine/ui/"
KA_WindowTimeout = 1000 * 60 * 5			# CLOSEWINDOWTIMEOUT

KA_Program = "wodim"					# BURNINGPROGRAM
KA_Device = "/dev/scd0"					# DEVICE
KA_LogFile = KA_BaseDir + "logs/active.txt"		# LOGFILE
