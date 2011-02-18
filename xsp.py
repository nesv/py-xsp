## @package xsp
# This is the main file for the XSP library.

import os
import xml.dom.minidom

class ParseException(Exception):
	def __init__(self, message):
		self.MESSAGE = message
	def __str__(self):
		return repr(self.MESSAGE)

def __parse_element(element, vocabulary):
	# Initialize the dictionary we are going to return.
	settings = {}
	
	# Every time we come across a new tag name in the vocabulary to parse,
	# we should create a new list to keep all of the gathered values in.
	for tag_name in vocabulary.keys():
		settings[tag_name] = []
		
		# Now, time to search through the root node and find all elements
		# with the same name as the current vocabulary term.
		# Every time we find a node to parse, append a new dictionary to
		# the list of attribute key-value pairs.
		for node in element.getElementsByTagName(tag_name):
			settings[tag_name].append({})
			
			# Here is where we actually do the main parsing.
			# For every attribute listed in the vocabulary tag's name,
			# check to make sure the current element node has that
			# attribute, and parse out the attribute by initially 
			# assigning it to a string (all values in the XML document
			# are treated as strings), the re-cast the value using the
			# function symbol provided as the value to the attribute-name
			# key, in the vocabulary.
			# Then, add the parse attribute value into a single-item
			# length list and re-case it using the map() function.
			for attribute in vocabulary[tag_name].keys():
				# Check to make sure the attribute we are looking at is
				# not None. If it is, it is a sub-vocabulary, so use the
				# magic of recursion to parse it out!
				if attribute == None:
					nested_element = __parse_element(node, vocabulary[tag_name][attribute])
					settings[tag_name][-1][attribute] = nested_element
				elif node.hasAttribute(attribute):
					a = str(node.getAttribute(attribute))
					a = map(vocabulary[tag_name][attribute], [a])
					settings[tag_name][-1][attribute] = a[0]
				else:
					print("WARNING: Element does not match vocabulary rule; skipping.")
					continue
	return settings

def parse(settings_file, vocabulary):
	# Check to make sure the vocabulary is a dictionary.
	if type(vocabulary) != type(dict()):
		print("ERROR: xsp.parse()")
		raise ParseException("The provided library is not a dictionary.")
	
	# Next, check to make sure the settings file does exist.
	if os.path.exists(settings_file):
		infile = xml.dom.minidom.parse(settings_file)
	else:
		raise ParseException("Provided path to settings file not valid; file does not exist")
	
	# Make sure the XML document is structured correctly.
	# There should be only one (1) child node when the file is open. From this
	# child node, all the other elements are below it.
	if len(infile.childNodes) == 1:
		root_node = infile.firstChild
	else:
		raise ParseException("Improperly formatted settings file; there is no document node.")
	
	# Return our settings.
	return __parse_element(root_node, vocabulary)

