all: day1

ifdef DEBUG
DEBUGFLGS = -g
else
DEBUGFLGS =
endif

day1: 1.S armmacros.s fileio.S
	gcc $(DEBUGFLGS) -o 1.app 1.S

%.o: %.s
	as $(DEBUGFLGS) $< -o $@

%.o: %.S
	gcc $(DEBUGFLGS) -c $< -o $@
