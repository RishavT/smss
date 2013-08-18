#!/usr/bin/python
import google
import os
homedir = os.getenv("HOME")
class Cont:
	def __init__(self):
		self.contacts = [('','')]
t = Cont()
def get(email,passwd):
	x = google.login(email,passwd)
	if x[0] == False:
		return x
	t.contacts = google.getcontacts()
	t.contacts.sort()
def write():
	if os.system("ls " + homedir + "/.smss/contacts") > 0:
		f = open("" + homedir + "/.smss/contacts","a")
		f.close()
	f = open("" + homedir + "/.smss/contacts","w")
	for x in t.contacts:
		f.write(x[0] + "\t" + x[1] + "\n")
	f.close()
def read():
	if os.system("ls " + homedir + "/.smss/contacts")>0:
		return False
	f = open("" + homedir + "/.smss/contacts","r")
	x = f.readlines()
	i = 0
	for y in x:
		a = y.split("\t")
		if a[1][-1]=='\n':
			a[1]=a[1][0:-1]
		if i == 0:
			t.contacts = [(a[0],a[1])]
		else:
			t.contacts += [(a[0],a[1])]
		i += 1
	t.contacts.sort()
def printc():
	for x in t.contacts:
		print x[0] + "\t" + x[1]
