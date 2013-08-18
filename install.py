#!/usr/bin/python
import sys
import os
f = open("installable","r")
if f.read()=="no":
	print "Please run make before installing"
else:
	if os.system("cp -R " + os.getcwd() + "/src/* /") <> 0:
		print "Please run with root previlages"
