import os
import re
from xml.dom.ext.reader import Sax2
from xml.dom.NodeFilter import NodeFilter
from xml.dom import minidom, Node

from settings import *

class Iso:
	def __init__(self):
		self.name = ''
		self.desc = ''
		self.url = ''
		self.image = ''
		self.file = ''

def populateIsoList():
		
	numIsos = 0
	isoList = []
	
	filelist = os.listdir(ISO_EnabledDir)
	filelist.sort()
	
	# for every file in the directory
	for filename in filelist:
		# find xml files
		if re.search('\.xml$', filename):
			
			# data about this iso will be stored in here:
			iso = Iso()
			
			# read the xml file
			reader = Sax2.Reader()
			doc = reader.fromStream("file://" + ISO_AvailDir + filename)
			
			print "\n" + "Adding content:"
			
			for node in doc.documentElement.childNodes:
				if node.nodeType == Node.ELEMENT_NODE:
					
					print node.nodeName + "\t-> " + node.firstChild.nodeValue
					
					if node.firstChild:
						nodeValue = node.firstChild.nodeValue
					else:
						continue
					
					# define things
					if node.nodeName == 'name':
						iso.name = nodeValue
					elif node.nodeName == 'desc':
						iso.desc = nodeValue
					elif node.nodeName == 'url':
						iso.url = nodeValue
					elif node.nodeName == 'image':
						iso.image = ISO_ImagePath + nodeValue
					elif node.nodeName == 'file':
						iso.file = ISO_AvailDir + nodeValue
					
			isoList.append(iso)
			numIsos += 1
		
		if numIsos >= ISO_MaxNumber:
			break
	print ''
	return isoList
