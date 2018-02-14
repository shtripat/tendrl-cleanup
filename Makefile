NAME = tendrl-cleanup
VERSION = 1.0.0
COMMIT := $(shell git rev-parse HEAD)
SHORTCOMMIT := $(shell echo $(COMMIT) | cut -c1-7)

all: srpm

clean:
	rm -rf $(NAME)-$(VERSION)
	rm -rf $(NAME)-$(VERSION).tar.gz
	rm -rf $(NAME)-$(VERSION)-*.el7.src.rpm

dist: clean
	mkdir $(NAME)-$(VERSION)
	cp -r roles $(NAME)-$(VERSION)
	cp .yamllint $(NAME)-$(VERSION)
	cp LICENSE $(NAME)-$(VERSION)
	cp README.md $(NAME)-$(VERSION)
	cp README.rpm.md $(NAME)-$(VERSION)
	cp site.yml.sample $(NAME)-$(VERSION)
	tar caf $(NAME)-$(VERSION).tar.gz $(NAME)-$(VERSION)

srpm: dist
	fedpkg --dist epel7 srpm

rpm: dist
	mock -r epel-7-x86_64 rebuild $(NAME)-$(VERSION)-*.src.rpm --resultdir=. --define "dist .el7"

gitversion:
	# Set version and release to the latest values from Git
	sed -i $(NAME).spec \
	  -e "/^Release:/cRelease: $(shell date +"%Y%m%dT%H%M%S").$(SHORTCOMMIT)"

snapshot: gitversion srpm


.PHONY: dist rpm srpm gitversion snapshot
