## @package xsp
# This is the main file for the XSP library.

import os
import xml.dom.minidom

class ParseException(Exception):
	def __init__(self, message):
		self.MESSAGE = message
	def __str__(self):
		return repr(self.MESSAGE)

class Settings:
	def __init__():
		pass
	
	def parse(self, settingsFile, vocabulary = None):
		if not vocabulary and not self.VOCABULARY:
			print("ERROR: xsp.Settings.parse()")
			raise ParseException("No vocabulary is defined.")
			return None
		
		if os.path.exists(settingsFile):
			infile = xml.dom.minidom.parse(settingsFile)
		else:
			raise ParseException("Provided path to settings file not valid; file does not exist")
			return None
	
	def set_vocabulary(self, vocabulary):
		if type(vocabulary) == type(dict()):
			self.VOCABULARY = vocabulary
		else:
			raise TypeError("Vocabulary must be a dict().")
	
	def get_vocabulary(self):
		if self.VOCABULARY:
			return self.VOCABULARY
		else:
			print("WARNING: Vocabulary has not been set.")
			return None
