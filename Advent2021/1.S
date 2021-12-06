// Advent of Code 2021 Day 1
// Included files are at https://github.com/SSteve/AdventOfCode/tree/master/Advent2021

// Registers:

// X19 - Current input buffer location.
// X20 - Address of first byte after input buffer.
// X21 - Previous value.
// X22 - one before previous value.
// X23 - two before previous value.
// X25 - Count for part 1.
// X26 - Count for part 2.
// X27 - Number of values read.

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
fileIsOpened:

	mov	X25, #0			// Initialize part 1 count.
	mov	X26, #0			// Initialize part 2 count.
	loadInteger			// Load the first value.
	mov	X27, #1			// Initialize number of values read.
	mov	X21, X0			// Set previous value to this value.

nextValue:
	loadInteger			// Load the next value.
	add	X27, X27, #1		// Increment number of values read.
	cmp	X0, #-1			// Did we reach the end of the input data?
	b.eq	done

	// For Part 1, we test to see if this value is larger than the previous value.
	cmp	X0, X21			// Is this greater than the previous value?
	cinc	X25, X25, hi		// If yes, increment part 1 count.

	cmp	X27, #4			// Have we read enough values to begin part 2?
	b.lo	copyPreviousValues	// If not, skip part 2 calculation.

	// For Part 2, we test to see if sum(z-3, z-2, z-1) > sum(z-2, z-1, z). We can simplify by
	// removing z-2 & z-1 from both sides of the inequality and simply test this value against
	// the third previous value.
	cmp	X0, X23			// Is this greater than the third previous value?
	cinc	X26, X26, hi		// If yes, increment part 2 count.

copyPreviousValues:
	mov	X23, X22		// Set third previous value to second previous value.
	mov	X22, X21		// Set second previous value to previous value.
	mov	X21, X0			// Set previous value to this value.
	b	nextValue

done:
	printVal	part1String, 25
	printVal	part2String, 26

exit:
	mov	X0, #0			// Return code
	pop1	LR
	ret

.data
fileName:
	.asciz	"1.txt"
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
