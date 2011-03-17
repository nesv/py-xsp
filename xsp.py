## @package xsp
# This is the main file for the XSP library.

import os
import xml.dom.minidom

class ParseException(Exception):
	def __init__(self, message):
		self.MESSAGE = message
	def __str__(self):
		return repr(self.MESSAGE)

def __parse_element(element, vocabulary, suppress_warnings):
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
					nested_element = __parse_element(node, 
									 vocabulary[tag_name][attribute], 
									 suppress_warnings)
					settings[tag_name][-1][attribute] = nested_element
				elif node.hasAttribute(attribute):
					a = str(node.getAttribute(attribute))
					a = map(vocabulary[tag_name][attribute], [a])
					settings[tag_name][-1][attribute] = a[0]
				else:
					if suppress_warnings:
						print("WARNING: Element does not match vocabulary rule; skipping.")
					continue
	return settings

def parse(settings_file, vocabulary, suppress_warnings = False):
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
	#
	# Addendum 20110316
	# It would appear that comments before the document node confuse xsp.
	# This is modified to attempt to find the actual child node where the
	# data is. Truth be told, it is not all that sophisticated; it just
	# goes with the first element that has child nodes.
	if len(infile.childNodes) == 1:
		root_node = infile.firstChild
	elif len(infile.childNodes) > 1:
		for node in infile.childNodes:
			if node.hasChildNodes():
				root_node = node
				break
	else:
		raise ParseException("Improperly formatted settings file; there is no document node.")
	
	# Return our settings.
	return __parse_element(root_node, vocabulary, suppress_warnings)

def yn2bool(s):
	"""bool yn2bool(str) - An added conversion function, to change
	"yes/no" values into boolean True and False values. If the parameter
	is not able to be parsed as a "yes/no" value, then this function
	returns nothing."""
	s = s.lower()
	if s == "yes" or s == "y":
		return True
	elif s == "no" or s == "n":
		return False
