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
	# Check to make sure the vocabulary is a dictionary.
	if type(vocabulary) != type(dict()):
		print("ERROR: xsp.Settings.parse()")
		raise ParseException("The provided library is not a dictionary.")
		return None
	
	# Next, check to make sure the settings file does exist.
	if os.path.exists(settingsFile):
		infile = xml.dom.minidom.parse(settingsFile)
	else:
		raise ParseException("Provided path to settings file not valid; file does not exist")
		return None
	
	# Make sure the XML document is structured correctly.
	# There should be only one (1) child node when the file is open. From this
	# child node, all the other elements are below it.
	if len(infile.childNodes) == 1:
		rootNode = infile.firstChild
	else:
		raise ParseException("Improperly formatted settings file; there is no document node.")
		return None
	
	# Now, it's time to actually do the parsing!
	# Initialize the dictionary we are going to return.
	settings = {}
	
	# Everytime we come across a new tag name to parse, in the vocabulary, we
	# should create a new list to keep all of the gathered values in.
	for tagName in vocabulary.keys():
		settings[tagName] = []
		
		# Now, time to search through the root node and find all elements with
		# the same name as the current vocabulary term.
		# Every time we find a node to parse, append a new dictionary to the
		# list of attribute key-value pairs.
		for node in rootNode.getElementsByTagName(tagName):
			settings[tagName].append({})
			
			# Here is where we actually do the main parsing.
			# For every attribute listed in the vocabulary tag's name, check
			# to make sure the current element node has that attribute, and
			# parse out the attribute by initially assigning it to a string
			# (all values in the XML document are treated as strings), then
			# re-cast the value using the function symbol provided as the value
			# to the attribute-name key, in the vocabulary.
			# Then, add the parse attribute value into a single-item length
			# list, and re-cast it using the map() function.
			for attribute in vocabulary[tagName].keys():
				if node.hasAttribute(attribute):
					a = str(node.getAttribute(attribute))
					a = map(vocabulary[tagName][attribute], [a])
					settings[tagName][-1][attribute] = a[0]
				else:
					print("WARNING: Element does not match vocabulary rule; skipping.")
					continue
	
	# Return our settings.
	return settings

