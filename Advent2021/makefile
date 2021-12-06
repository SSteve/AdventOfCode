all: 1.app # 2.app 3.app 4.app

ifdef DEBUG
DEBUGFLGS = -g
else
DEBUGFLGS =
endif

1.app: 1.S armmacros.s fileio.S
	gcc $(DEBUGFLGS) -o 1.app 1.S

#2.app: 2.S armmacros.s fileio.S
#	gcc $(DEBUGFLGS) -o 2.app 2.S

#3.app: 3.S armmacros.s fileio.S
#	gcc $(DEBUGFLGS) -o 3.app 3.S

#4.app: 4.S armmacros.s fileio.S
#	gcc $(DEBUGFLGS) -o 4.app 4.S
