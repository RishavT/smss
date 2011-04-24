#This is the makefile.
all:
	python check.py
	python -m compileall postinst.py
install:
	python install.py
