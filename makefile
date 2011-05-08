#This is the makefile.
all:
	python check.py
	python -m compileall google.py Contacts.py sms.py
	cp google.pyc Contacts.pyc sms.pyc src/usr/share/smss
install:
	python install.py
