// Various macros to perform file I/O
//
// The fd parameter needs to be a register.
// Uses X0, X1, X8.
// Return code is in X0.

#include <asm/unistd.h>

.equ  O_RDONLY, 0
.equ  O_WRONLY, 1
.equ  O_CREAT,  0100
.equ  O_EXCL,   0200
.equ  S_RDWR,   0666
.equ  AT_FDCWD, -100

.macro	openFile	fileName, flags
	mov	x0, #AT_FDCWD
	ldr	x1, =\fileName
	mov	x2, #\flags
	mov	x3, #S_RDWR	// r/w access rights
	mov	x8, #__NR_openat
	svc	0
.endm

// Read file into statically allocated memory.
.macro	readFile	fd, buffer, length
	mov	x0, \fd		// file descriptor
	ldr	x1, =\buffer
	mov	x2, #\length
	mov	x8, #__NR_read
	svc	0
.endm

// Read file into dynamically memory.
.macro readFileDynamic	fd, reg, length
	mov	x0, \fd
	mov	x1, \reg
	mov	x2, #\length
	mov	x8, #__NR_read
	svc	0
.endm

.macro	writeFile	fd, buffer, length
	mov	X0, \fd      // file descriptor
	ldr	X1, =\buffer
	mov	X2, \length
	mov	X8, #__NR_write
	svc	0
.endm

.macro	flushClose	fd
// fsync syscall
	mov	x0, \fd
	mov	x8, #__NR_fsync
	svc	0
// close syscall
	mov	x0, \fd
	mov	x8, #__NR_close
	svc	0
.endm
