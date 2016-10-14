#
# Build mock and local RPM versions of tools
#

# Assure that sorting is case sensitive
LANG=C

MOCKS+=fedora-24-x86_64
MOCKS+=epel-7-x86_64
MOCKS+=epel-6-x86_64
MOCKS+=epel-5-x86_64

SPEC := `ls *.spec | head -1`
PKGNAME := "`ls *.spec | head -1 | sed 's/.spec$$//g'`"

NAME := mydumper
VERSION := 0.9.1
MAJORVERSION := 0.9

TARBALL := $(NAME)-$(VERSION).tar.gz

all:: verifyspec $(TARBALL) $(MOCKS)

# Oddness to get deduced .spec file verified
verifyspec:: FORCE
	@if [ ! -e $(SPEC) ]; then \
	    echo Error: SPEC file $(SPEC) not found, exiting; \
	    exit 1; \
	fi

.PHONY: tarball
tarball: $(TARBALL)
$(TARBALL):
	wget 'http://launchpad.net/$(NAME)/$(MAJORVERSION)/$(VERSION)/+download/$(TARBALL)'

srpm:: verifyspec FORCE
	@echo "Building SRPM with $(SPEC)"
	rm -rf rpmbuild
	rpmbuild --define '_topdir $(PWD)/rpmbuild' \
		 --define '_sourcedir $(PWD)' \
		 -bs $(SPEC) --nodeps

build:: srpm FORCE
	rpmbuild --define '_topdir $(PWD)/rpmbuild' \
		 --rebuild $(PWD)/rpmbuild/SRPMS/*.src.rpm

$(MOCKS):: verifyspec FORCE
	@if [ -e $@ -a -n "`find $@ -name \*.rpm`" ]; then \
		echo "Skipping RPM populated $@"; \
	else \
		echo "Building $@ RPMS with $(SPEC)"; \
		rm -rf $@; \
		/usr/bin/mock -q -r $@ --sources=$(PWD) \
		    --resultdir=$(PWD)/$@ \
		    --buildsrpm --spec=$(SPEC); \
		echo "Storing $@/*.src.rpm in $@.rpm"; \
		/bin/mv $@/*.src.rpm $@.src.rpm; \
		echo "Actally building RPMS in $@"; \
		rm -rf $@; \
		/usr/bin/mock -q -r $@ \
		     --resultdir=$(PWD)/$@ \
		     $@.src.rpm; \
	fi

mock:: $(MOCKS)

clean::
	rm -rf $(MOCKS)
	rm -rf rpmbuild

realclean distclean:: clean
	rm -f *.src.rpm
	rm -f $(TARBALL)

FORCE:
