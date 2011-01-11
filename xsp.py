## @package xsp
# This is the main file for the XSP library.

import os
import xml.dom.minidom

class ParseException(Exception):
	def __init__(self, message):
		self.MESSAGE = message
	def __str__(self):
		return repr(self.MESSAGE)

def parse(settingsFile, vocabulary):
	if not vocabulary:
		print("ERROR: xsp.Settings.parse()")
		raise ParseException("No vocabulary is defined.")
		return None
	
	if os.path.exists(settingsFile):
		infile = xml.dom.minidom.parse(settingsFile)
	else:
		raise ParseException("Provided path to settings file not valid; file does not exist")
		return None
	
	if len(infile.childNodes) == 1:
		rootNode = infile.firstChild
	else:
		raise ParseException("Improperly formatted settings file; there is no document node.")
		return None
	
	settings = {}
	for tagName in vocabulary.keys():
		settings[tagName] = []

		for node in rootNode.getElementsByTagName(tagName):
			settings[tagName].append({})

			for attribute in vocabulary[tagName].keys():
				if node.hasAttribute(attribute):
					a = str(node.getAttribute(attribute))
					a = map(vocabulary[tagName][attribute], [a])
					settings[tagName][-1][attribute] = a[0]
				else:
					print("WARNING: Element does not match vocabulary rule; skipping.")
					continue
	
	return settings

class Settings:
	def __init__():
		pass
	
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
