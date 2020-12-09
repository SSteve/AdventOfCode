all: day1 day2 day3

ifdef DEBUG
DEBUGFLGS = -g
else
DEBUGFLGS =
endif

day1: 1.S armmacros.s fileio.S
	gcc $(DEBUGFLGS) -o 1.app 1.S

day2: 2.S armmacros.s fileio.S
	gcc $(DEBUGFLGS) -o 2.app 2.S

day3: 3.S armmacros.s fileio.S
	gcc $(DEBUGFLGS) -o 3.app 3.S

%.o: %.s
	as $(DEBUGFLGS) $< -o $@

%.o: %.S
	gcc $(DEBUGFLGS) -c $< -o $@
