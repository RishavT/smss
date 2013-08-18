#This is the makefile.
all:
	python check.py
	python -m compileall google.py Contacts.py sms2.py
	cp google.pyc Contacts.pyc sms2.pyc src/usr/share/smss
install:
	python install.py
