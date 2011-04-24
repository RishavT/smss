#!/usr/bin/python
import os
def do():
	dirs = os.popen("ls /home")
	directory = dirs.readlines()
	print "checking for previous installations.."
	if os.system("ls /usr/bin/nfuploader") == 0:
		os.system("rm /usr/bin/nfuploader")
	os.system("ln -s /usr/share/nfuploader/Facebook.py /usr/bin/nfuploader")
	for x in directory:
		print "checking for previous installations.."
		y = os.system("ls '/home/" + x[0:-1] + "/.gnome2/nautilus-scripts/Upload To Facebook'")
		if y==0:
			os.system("rm '/home/" + x[0:-1] + "/.gnome2/nautilus-scripts/Upload To Facebook'")
		os.system("touch '/home/" + x[0:-1] + "/.gnome2/nautilus-scripts/Upload To Facebook'")
		try:
			f = open("/home/" + x[0:-1] + "/.gnome2/nautilus-scripts/Upload To Facebook", 'w')
			f.write("#!/bin/bash\nnfuploader $@")
			f.close()
			os.system("chmod +x '/home/" + x[0:-1] + "/.gnome2/nautilus-scripts/Upload To Facebook'")
		except Exception:
			pass
	print "Installation complete!"
