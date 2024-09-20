sources = devboard.pld

all: $(sources:.pld=.jed)
	@ls -lh "$^"

GALasm:
	git submodule update $@

GALasm/src/galasm: GALasm
	make -C GALasm/src galasm

%.jed:	%.pld GALasm/src/galasm Makefile
	GALasm/src/galasm -v $<

clean:
	rm -f $(sources:.pld=.jed)

.PHONY: all clean
