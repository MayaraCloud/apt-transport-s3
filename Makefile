#!/usr/bin/make
# vim: tabstop=4 softtabstop=4 noexpandtab fileencoding=utf-8

DIRS:= src

.PHONY: clean

all:
	clean
	deb

clean:
	rm -rf debian/apt-transport-s3*

deb:
	dpkg-buildpackage -us -uc
