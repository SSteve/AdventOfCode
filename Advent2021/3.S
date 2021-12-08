// Advent of Code 2021 Day 2
// Included files are at https://github.com/SSteve/AdventOfCode/tree/master/Advent2021

#include <asm/unistd.h>
#include "fileio.S"
#include "armmacros.s"
#include "armutilities.s"

.equ	BUFFERLEN,	14000
// Number of 32-bit values we want to reserve memory for.
.equ	RESERVED_VALUES_COUNT,	1000

.global	main

////////////////////////////////////////////////////////
// Count the number of bits in each puzzle value.
////////////////////////////////////////////////////////
getBitWidth:
// Input:
// X0 - pointer into buffer.
// Output:
// X0 - number of bits in the puzzle values.
// Registers used:
// X1 - Original buffer start.
// W2 - character loaded from buffer.

	mov	X1, X0			// Save the initial buffer start.
bwNextValue:
	ldrb	W2, [X0], #1		// Load next character and increment pointer.
	cmp	W2, #'0'		// Is this less than '0'?
	b.lo	bwDone			// Yes, we've reached the end of the first value.
	cmp	W2, #'1'		// Is this greater than '1'?
	b.hi	bwDone			// Yes, we've reached the end of the first value.
	b bwNextValue			// Examine the next value.
bwDone:
	sub	X0, X0, X1		// Subtract start from pointer to get characters read.
	sub	X0, X0, #1		// Subtract one because the last character read wasn't a valid bit.
	ret

main:
// Registers:
// X19 - Current input buffer location.
// X20 - Address of first byte after input buffer.
// X21 - Number of bits in puzzle values.
// X22 - Number of puzzle values.
// FP  - Pointer to memory allocated with malloc.
	push2	LR, FP

	// Allocate memory for our values.
	mov	X0, #RESERVED_VALUES_COUNT << 2
	bl	malloc
	mov	FP, X0

	// Load the file.
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
fileIsLoaded:
	mov	X22, #0			// Initialize the number of puzzle values.

// Find the number of bits in the puzzle values.
	mov	X0, X19
	bl	getBitWidth
	mov	X21, X0

// Convert the string representations to binary.
loadValues:
	mov	X1, X20			// Copy end of buffer to argument.
	mov	X0, X19			// Copy current buffer location to argument.
	bl	loadBinaryValue		// Get the next value from the buffer.
	mov	X19, X1			// Copy the new buffer position into our buffer pointer.

	cmp	X0, #-1			// Was there another value?
	b.eq	finishedLoadingValues	// No more values, start processing.

	str	W0, [FP, X22, lsl #2]	// Store the loaded value.
	add	X22, X22, #1		// Increase the number of values loaded.
	b loadValues

// Start the puzzle.
// Registers in this section
// X0 - the value we're testing.
// X1 - loop variable for counting bits.
// X2 - loop variable for processing values.
// X3 - bit flag for inverting gamma to obtain epsilon.
// X4 - counter for set bits.
// X5 - mask for testing set bits.
// X6 - number of values / 2 for testing.
// X7 - gamma value.
// X8 - epsilon value.
finishedLoadingValues:
	// Create bit flag. It is 2^(number_of_bits + 1) - 1. i.e. if there are five bits,
	// we want a value with five ones so we subtract 1 from 2^6 to get 0b11111.
	mov	X3, #1
	lsl	X3, X3, X21		// We now have 2^(number_of_bits + 1)
	lsr	X5, X3, #1		// Shift this right once to get our mask for bit testing.
	sub	X3, X3, #1		// Our flag for inverting bits now has a 1 in every bit position.

	// Calculate the number to test against to see which bit value we use.
	asr	X6, X22, #1		// The test value is the number of values / 2.

	mov	X7, #0			// Initialize gamma value.
	mov	X1, #0			// Initialize loop variable for bit testing.
	// while X1 < X21 count bits.
processNextBit:
	mov	X2, #0			// Initialize loop variable for value testing.
	mov	X4, #0			// Initialize bit count.
	// while X2 < X22 process next value
processNextValue:
	ldr	W0, [FP, X2, lsl #2]	// Load the value.
	tst	X0, X5			// Test this bit.
	cinc	X4, X4, ne		// If set, increment counter.

	add	X2, X2, #1		// Increment the loop counter.
	cmp	X2, X22			// Is this the last value?
	b.lo	processNextValue	// No, process the next value.

	// We've finished counting the bits in this position.
	lsl	X7, X7, #1		// Shift gamma.
	cmp	X4, X6			// Is bit count >= number of values / 2?
	cset	X0, hi			// If yes, set X0.
	orr	X7, X7, X0		// Add X0 to gamma.

	lsr	X5, X5, #1		// Shift our test mask right.

	add	X1, X1, #1		// Increment value counter.
	cmp	X1, X21			// Are we finished with all the bits?
	b.lo	processNextBit		// No, process the next bit.

	// Now we have gamma. Invert its bits to get epsilon.
	eor	X8, X7, X3

	// Multiply gamma and epsilon to get our answer.
	mul	X0, X8, X7

	printVal	part1String, 0

exit:
	mov	X0, FP
	bl	free
	mov	X0, #0			// Return code
	pop2	LR, FP
	ret

.data
fileName:
	.asciz	"3.txt"
//	.asciz	"3test.txt"
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
