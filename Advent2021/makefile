all: 1.app 2.app 3.app 4.app 5.app

ifdef DEBUG
DEBUGFLGS = -g
else
DEBUGFLGS =
endif

%.o: %.s
	as $(DEBUGFLGS) $< -o $@
	
1.app: 1.S armmacros.s fileio.S
	gcc $(DEBUGFLGS) -o 1.app 1.S

2.app: 2.S armmacros.s fileio.S
	gcc $(DEBUGFLGS) -o 2.app 2.S

3.app: 3.S armmacros.s fileio.S armutilities.s
	gcc $(DEBUGFLGS) -o 3.app 3.S

4.app: 4.S armmacros.s fileio.S
	gcc $(DEBUGFLGS) -o 4.app 4.S

5.app: 5.S armmacros.s fileio.S armutilities.s
	gcc $(DEBUGFLGS) -o 5.app 5.S
