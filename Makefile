PACKAGE = $(shell sed -ne "s/^name=//p" metadata.txt)
VERSION = $(shell sed -ne "s/^version=//p" metadata.txt)
LPACKAGE = $(shell echo $(PACKAGE) | tr [:upper:] [:lower:])

zip: $(LPACKAGE)-$(VERSION).zip

resources.py: resources.qrc
	pyrcc4 -o $@ $^

$(LPACKAGE)-$(VERSION).zip: resources.py
	git archive --format zip --prefix=$(LPACKAGE)/ HEAD >$(LPACKAGE)-$(VERSION).zip
