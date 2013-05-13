#!/usr/bin/python
f = open("installable",'w')
boolean = True
print "Checking for dependencies..."
x = "wx -> present"
try:
	import wx
except ImportError:
	x = "wx -> NOT FOUND"
	boolean = False
print x
x = "python-gdata -> present"
try:
	import gdata.service
	import gdata.calendar.service
	import gdata.docs.service
	import gdata.contacts.client
	import gdata.contacts.service
except ImportError:
	x = "python-gdata -> NOUT FOUND"
	boolean = False
print x
x = "urllib / httplib2 -> present"
try:
	import urllib
	import httplib2
	import random
except ImportError:
	x = "urllib / httplib2 -> NOT FOUND"
	boolean = False
print x
x = "pyrucl -> present"
if boolean:
	f.write("yes")
else:
	f.write("no")
f.close()
