#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
import gtk, gobject, webkit, os
import burn, contentparser, log

from settings import *

gobject.threads_init()
os.system("sh " + KA_BaseDir + "calibrate.sh")

class wlhska (gtk.Window):

	def __init__ (self):
		gtk.Window.__init__(self)
		#self.set_title("main.py - WLFT-KA")
		self.set_title("IdatuxFT")
		self.connect("destroy", gtk.main_quit)
		self.set_default_size(KA_ScreenResolution[0], KA_ScreenResolution[1])
		self.fullscreen()
		
		self.layout = gtk.VBox()
		
		self.toastertitle = gtk.Label()
		self.toastertitle.set_label("<b><span size='36000'>" + KA_Name + "</span></b>")
		self.toastertitle.set_use_markup(True)
		self.toastertitle.set_selectable(False)
		self.toastertitle.set_justify(gtk.JUSTIFY_CENTER)
		
		self.subtitle = gtk.Label()
		self.subtitle.set_label("<span size='16000'>Presiona en el botón que te interesa para ver la información y grabar tu CD.</span>")
		self.subtitle.set_use_markup(True)
		self.subtitle.set_selectable(False)
		self.subtitle.set_justify(gtk.JUSTIFY_CENTER)
		
		self.padding = gtk.Label("<span size='9000'> </span>")
		self.padding.set_use_markup(True)
		self.padding.set_selectable(False)
		self.padding.set_justify(gtk.JUSTIFY_CENTER)
		
		self.layout.pack_start(self.toastertitle, False)
		self.layout.pack_start(self.subtitle, False)
		self.layout.pack_start(self.padding, False)
		
		# Software buttons
		self.buttontable = gtk.VBox(True)
		
		# Insert automated button adding function here.
		isoList = contentparser.populateIsoList()
		numAdded = 0
		for iso in isoList:
			if numAdded % 2 == 0:
				hbox = gtk.HBox(True)
				self.layout.pack_start(hbox, True, True)
				hbox.show()
				
			button = gtk.Button()
			button.set_focus_on_click(False)
			button.connect("clicked", detailScreen, iso)
			hbox.pack_start(button, True, True)
			button.show()
			
			buttonTextWidth = 400
			populateButton(button, iso)
			numAdded += 1
		
		# Help/about buttons
		self.infobuttons = gtk.Table(1, 3, True)
		
		# Help button
		helpbutton = gtk.Button()
		helpbutton.set_focus_on_click(False)
		helpbutton.connect("clicked", helpScreen)
		
		icon = gtk.Image()
		icon.set_from_file(KA_UIDir + 'main.help.png')
		label = gtk.Label("<span size='24000'>Ayuda</span>")
		label.set_use_markup(True)
		
		layout = gtk.HBox(False, 10)
		
		layout.pack_start(icon, False, False)
		layout.pack_start(label, True, True)
		
		icon.show()
		label.show()
		
		helpbutton.add(layout)
		self.infobuttons.attach(helpbutton, 0, 1, 0, 1)
		
		# About button
		aboutbutton = gtk.Button()
		aboutbutton.set_focus_on_click(False)
		aboutbutton.connect("clicked", aboutScreen)
		
		icon = gtk.Image()
		icon.set_from_file(KA_UIDir + 'main.about.png')
		label = gtk.Label("<span size='24000'>El proyecto</span>")
		label.set_use_markup(True)
		
		layout = gtk.HBox(False, 10)
		
		layout.pack_start(icon, False, False)
		layout.pack_start(label, True, True)
		
		icon.show()
		label.show()
		
		aboutbutton.add(layout)
		self.infobuttons.attach(aboutbutton, 1, 2, 0, 1)

		# People button
		peoplebutton = gtk.Button()
		peoplebutton.set_focus_on_click(False)
		peoplebutton.connect("clicked", peopleScreen)
		
		icon = gtk.Image()
		icon.set_from_file(KA_UIDir + 'main.people.png')
		label = gtk.Label("<span size='24000'>Idatux</span>")
		label.set_use_markup(True)
		
		layout = gtk.HBox(False, 10)
		
		layout.pack_start(icon, False, False)
		layout.pack_start(label, True, True)
		
		icon.show()
		label.show()
		
		peoplebutton.add(layout)
		self.infobuttons.attach(peoplebutton, 2, 3, 0, 1)
		
		# Hide the cursor
		'''
		pix_data = """/* XPM */
		static char * invisible_xpm[] = {
		"1 1 1 1",
		"       c None",
		" "};"""
		color = gtk.gdk.Color()
		pix = gtk.gdk.pixmap_create_from_data(None, pix_data, 1, 1, 1, color, color)
		invisible = gtk.gdk.Cursor(pix, pix, color, color, 0, 0)
		gdkWindow = self.get_screen().get_root_window()
		gdkWindow.set_cursor(invisible)
		'''
		
		self.layout.pack_start(self.buttontable, False)
		self.layout.pack_start(self.infobuttons, False)
		self.add(self.layout)

	# Se definen los botones con las distribuciones para grabar

def populateButton(button, iso):

	# picture
	icon = gtk.Image()
	icon.set_from_file(iso.image)

	# iso name
	title = gtk.Label('<span size="17000"><b>' + iso.name + '</b></span>')
	title.set_use_markup(True)
	
	# iso description
	desc = gtk.Label('<span size="12000">' + iso.desc + '</span>')
	desc.set_use_markup(True)
	desc.set_line_wrap(True)
	
	layout = gtk.Table(2, 2, False)
	layout.attach(icon, 0, 1, 1, 2)
	layout.attach(title, 0, 2, 0, 1, gtk.SHRINK, gtk.SHRINK)
	layout.attach(desc, 1, 2, 1, 2, gtk.EXPAND, gtk.EXPAND)
	
	icon.show()
	title.show()
	desc.show()
	
	button.add(layout)
	
	return layout, title

# Opens the details screen before burning.
def detailScreen(button, iso):
	
	log.logMessage("ViewISODetails", iso.name, iso.file)

	detailsWindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
	detailsWindow.set_title(iso.name + " - IdatuxFT")
	detailsWindow.set_default_size(KA_ScreenResolution[0], KA_ScreenResolution[1])
	detailsWindow.fullscreen()

	# Details view
	details = webkit.WebView()
	details.set_editable(False)
	details.load_html_string("<h1>Cargando URL</h1>", "file:///")
	details.open(ISO_AvailDir + iso.url)

	scroll = gtk.ScrolledWindow()
	scroll.add(details)
	scroll.set_policy(gtk.POLICY_ALWAYS, gtk.POLICY_NEVER)
	
	# Button bar
	buttonbar = gtk.Table(1, 2, True)
	
	# Back button
	backbutton = gtk.Button()
	backbutton.set_focus_on_click(False)
	backbutton.connect("clicked", burn.closeWindowAndEjectCbk, detailsWindow)
	
	icon = gtk.Image()
	icon.set_from_file(KA_UIDir + 'details.back.png')
	label = gtk.Label("<span size='24000'>Menú principal</span>")
	label.set_use_markup(True)
	
	layout = gtk.HBox(False, 10)
	
	layout.pack_start(icon, False, False)
	layout.pack_start(label, True, True)
	
	backbutton.add(layout)
	buttonbar.attach(backbutton, 0, 1, 0, 1)
	
	# Burn button
	burnbutton = gtk.Button()
	burnbutton.set_focus_on_click(False)
	burnbutton.connect("clicked", burn.burn, iso.file)
	
	icon = gtk.Image()
	icon.set_from_file(KA_UIDir + 'details.burn.png')
	label = gtk.Label("<span size='24000'>Grabar Disco</span>")
	label.set_use_markup(True)
	
	os.system("eject ")
	
	
	layout = gtk.HBox(False, 10)
	
	layout.pack_start(icon, False, False)
	layout.pack_start(label, True, True)
	
	burnbutton.add(layout)
	buttonbar.attach(burnbutton, 1, 2, 0, 1)
	
	layout = gtk.VBox()
	layout.pack_start(scroll, True, True)
	layout.pack_start(buttonbar, False, False)
	detailsWindow.add(layout)
	
	detailsWindow.show_all()
	
	gobject.timeout_add(KA_WindowTimeout, detailsWindow.destroy)
	
# Show the help screen
def helpScreen(button):
	log.logMessage("HelpScreen", "", "")
	
	helpWindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
	helpWindow.set_title("ayuda.html - IdatuxFT")
	helpWindow.set_default_size(KA_ScreenResolution[0], KA_ScreenResolution[1])
	helpWindow.fullscreen()

	# Details view
	details = webkit.WebView()
	details.set_editable(False)
	details.open(KA_HelpFile)

	scroll = gtk.ScrolledWindow()
	scroll.add(details)
	scroll.set_policy(gtk.POLICY_ALWAYS, gtk.POLICY_NEVER)
	
	# Button bar
	buttonbar = gtk.Table(1, 1, True)
	
	# Back button
	backbutton = gtk.Button()
	backbutton.set_focus_on_click(False)
	backbutton.connect("clicked", close_window)
	
	icon = gtk.Image()
	icon.set_from_file(KA_UIDir + 'details.back.png')
	label = gtk.Label("<span size='24000'>Menú Principal</span>")
	label.set_use_markup(True)
	
	layout = gtk.HBox(False, 10)
	
	layout.pack_start(icon, False, False)
	layout.pack_start(label, True, True)
	
	backbutton.add(layout)
	buttonbar.attach(backbutton, 0, 1, 0, 1)
	
	layout = gtk.VBox()
	layout.pack_start(scroll, True, True)
	layout.pack_start(buttonbar, False, False)
	helpWindow.add(layout)
	
	helpWindow.show_all()
	
	gobject.timeout_add(KA_WindowTimeout, helpWindow.destroy)
	
def peopleScreen(button):
	log.logMessage("HelpScreen", "", "")
	
	peopleWindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
	peopleWindow.set_title("ayuda.html - IdatuxFT")
	peopleWindow.set_default_size(KA_ScreenResolution[0], KA_ScreenResolution[1])
	peopleWindow.fullscreen()

	# Details view
	details = webkit.WebView()
	details.set_editable(False)
	details.open(KA_AuthorsFile)

	scroll = gtk.ScrolledWindow()
	scroll.add(details)
	scroll.set_policy(gtk.POLICY_ALWAYS, gtk.POLICY_NEVER)
	
	# Button bar
	buttonbar = gtk.Table(1, 1, True)
	
	# Back button
	backbutton = gtk.Button()
	backbutton.set_focus_on_click(False)
	backbutton.connect("clicked", close_window)
	
	icon = gtk.Image()
	icon.set_from_file(KA_UIDir + 'details.back.png')
	label = gtk.Label("<span size='24000'>Menú Principal</span>")
	label.set_use_markup(True)
	
	layout = gtk.HBox(False, 10)
	layout.pack_start(icon, False, False)
	layout.pack_start(label, True, True)
	
	backbutton.add(layout)
	buttonbar.attach(backbutton, 0, 1, 0, 1)
	
	layout = gtk.VBox()
	layout.pack_start(scroll, True, True)
	layout.pack_start(buttonbar, False, False)
	peopleWindow.add(layout)
	
	peopleWindow.show_all()
	
	gobject.timeout_add(KA_WindowTimeout, peopleWindow.destroy)
	
def aboutScreen(button):
	log.logMessage("HelpScreen", "", "")
	
	aboutWindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
	aboutWindow.set_title("ayuda.html - IdatuxFT")
	aboutWindow.set_default_size(KA_ScreenResolution[0], KA_ScreenResolution[1])
	aboutWindow.fullscreen()

	# Details view
	details = webkit.WebView()
	details.set_editable(False)
	details.open(KA_AboutFile)

	scroll = gtk.ScrolledWindow()
	scroll.add(details)
	scroll.set_policy(gtk.POLICY_ALWAYS, gtk.POLICY_NEVER)
	
	# Button bar
	buttonbar = gtk.Table(1, 1, True)
	
	# Back button
	backbutton = gtk.Button()
	backbutton.set_focus_on_click(False)
	backbutton.connect("clicked", close_window)
	
	icon = gtk.Image()
	icon.set_from_file(KA_UIDir + 'details.back.png')
	label = gtk.Label("<span size='24000'>Menú Principal</span>")
	label.set_use_markup(True)
	
	layout = gtk.HBox(False, 10)
	
	layout.pack_start(icon, False, False)
	layout.pack_start(label, True, True)
	
	backbutton.add(layout)
	buttonbar.attach(backbutton, 0, 1, 0, 1)
	
	layout = gtk.VBox()
	layout.pack_start(scroll, True, True)
	layout.pack_start(buttonbar, False, False)
	aboutWindow.add(layout)
	
	aboutWindow.show_all()
	
	gobject.timeout_add(KA_WindowTimeout, aboutWindow.destroy)

def close_window(button):
	button.get_parent_window().destroy()
	
wlhska().show_all()
gtk.main()
