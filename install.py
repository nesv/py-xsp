#!/usr/bin/env python

import sys, os, shutil

FILES = ["xsp.py"]

def install_to_path(path):
	if type(path) == type(str()):
		try:
			for f in FILES:
				shutil.copy(f, path)
				print("Installed %s to %s" % (f, path))
		except IOError, e:
			print("Installation failed; %s" % str(e))
		except shutil.Error, e:
			print("Installation failed; %s" % str(e))

def install():
	print("The following directories are in your Python path:")
	for p in sys.path[1:]:
		print("\t%s" % p)
	print("Please type in the path you would like to install to.")
	while True:
		answer = raw_input("> ").strip()
		if (answer in sys.path[1:]) or os.path.exists(answer):
			install_successful = install_to_path(answer)
			if install_successful:
				print("--- py-xsp successfully installed! -------------------")
			break
		else:
			print("That directory does not exist; try again.")
			continue

if __name__ == "__main__":
	print("--- Installing xsp -----------------------------------------------")
	try:
		install()
	except KeyboardInterrupt:
		print("\nTerminating on user request.")
		print("Goodbye.")
