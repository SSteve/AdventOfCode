// Advent of Code 2021 Day 2
// Included files are at https://github.com/SSteve/AdventOfCode/tree/master/Advent2021

// Registers:

// X0  - Next numeric value after invoking loadInteger
// X19 - Current input buffer location.
// X20 - Address of first byte after input buffer.
// X21 - Position.
// X22 - Depth for part 1 and Aim for part 2.
// X23 - Depth for part 2.
// W24 - First character in current command.

#include <asm/unistd.h>
#include "fileio.S"
#include "armmacros.s"

.equ	BUFFERLEN,	10000

.global	main

main:
	push1	LR

	openFile	fileName, O_RDONLY
	adds	X9, xzr, X0		// Save file descriptor.
	b.pl	openOk			// Positive value means file is open.
	mov	X1, #1			// stdout
	ldr	X2, =inputErrorLen	// Error message length.
	ldr	W2, [X2]
	writeFile	X1, inputError, X2	// Print the error message.
	b	exit

	// File opened successfully.
openOk:
	// Read the entire file into the buffer.
	readFile	X9, buffer, BUFFERLEN
	ldr	X19, =buffer		// Start at beginning of buffer.
	add	X20, X19, X0		// End of buffer is buffer address plus
					//  X0 which contains the number of characters read.
	flushclose X9

	// Initialize values
	mov	X21, #0
	mov	X22, #0
	mov	X23, #0

processNextLine:
	cmp	X19, X20		// If we're at the end of the input buffer, we're done.
	b.eq	done

	ldrb	W24, [X19], #1		// Get the first character of the next command

	// Check to see if this is a lower-case character. If not, go to next character.
	cmp	W24, #'a'
	b.lo	processNextLine
	cmp	W24, #'z'
	b.hi	processNextLine

	loadInteger
	cmp	X0, #-1			// If there isn't another value, we're done.
	b.eq	done

	cmp	W24, #'f'		// Process 'forward' command.
	b.ne	depthCommand
	add	X21, X21, X0
	madd	X23, X22, X0, X23
	b processNextLine

depthCommand:
	cmp	W24, #'d'		// Process 'down' command.
	b.ne	upCommand
	add	X22, X22, X0
	b processNextLine

upCommand:
	sub	X22, X22, X0		// Process 'up' command.
	b processNextLine

done:
	mul	X3, X21, X22
	mul	X4, X21, X23
	printVal	part1String, 3
	printVal	part2String, 4

exit:
	mov	X0, #0			// Return code
	pop1	LR
	ret

.data
fileName:
	.asciz	"2.txt"
buffer:
	.fill	BUFFERLEN + 1, 1, 0
inputError:
	.asciz	"Failed to open input file.\n"
inputErrorLen:
	.word	. - inputError
part1String:
	.asciz "Part1: "
part2String:
	.asciz "Part2: "


