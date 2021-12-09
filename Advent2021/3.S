// Advent of Code 2021 Day 2
// Included files are at https://github.com/SSteve/AdventOfCode/tree/master/Advent2021

#include <asm/unistd.h>
#include "fileio.S"
#include "armmacros.s"
#include "armutilities.s"

.equ	BUFFERLEN,	14000
// Number of 32-bit values we want to allocate memory for.
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

////////////////////////////////////////////////////////
// Main
////////////////////////////////////////////////////////
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
	b.eq	part1			// No more values, start processing.

	str	W0, [FP, X22, lsl #2]	// Store the loaded value.
	add	X22, X22, #1		// Increase the number of values loaded.
	b loadValues

// Start the puzzle.
// Registers in this section:
// X0 - the value we're testing.
// X1 - loop variable for counting bits.
// X2 - loop variable for processing values.
// X3 - bit flag for inverting gamma to obtain epsilon.
// X4 - counter for set bits.
// X5 - mask for testing set bits.
// X6 - number of values / 2 for testing.
// X7 - gamma value.
// X8 - epsilon value.
part1:
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
	// do while X1 < X21 count bits.
processNextBit:
	mov	X2, #0			// Initialize loop variable for value testing.
	mov	X4, #0			// Initialize bit count.
	// do while X2 < X22 process next value
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

// In part two, we'll copy the values and then remove them as they are eliminated from contention.
// We can re-use the buffer we loaded the file into since that has already been converted into our
// binary values.
// Registers in this section:
// X0 - The value we're testing.
// X1 - loop variable for counting bits.
// X2 - loop variable for processing values.
// X3 - Mask for testing set bits.
// X4 - The number of valid values remaining.
// X5 - The pointer to the buffer.
// X7 - Bit count.
// X8 - 1 if we keep values with 1, 0 if we keep values with 0.
// X9 - Index we're copying to when removing values.
// X10 - Index we're copying from when removing values.
// X11 - Flag for first or second pass.
// X12 - Oxygen generator rating (pass 1)
// X13 - CO2 scrubber rating (pass 2)
part2:
	// When the X11 flag is 1 we're on the first pass where we use the most common bit.
	mov	X11, #1

part2PassStart:
	// Copy the values to the buffer.
	ldr	X5, =buffer
	mov	X2, #0			// Initialize the index value.
copyNextValue:
	ldr	W0, [FP, X2, lsl #2]	// Load the value.
	str	W0, [X5, X2, lsl #2]	// Store the value into the buffer.
	add	X2, X2, #1
	cmp	X2, X22			// Have we written all the values?
	b.lo	copyNextValue		// No, copy the next value.

	mov	X4, X22			// All the values are valid to start.

	// We've finished copying the values to the buffer. Now we count bits and filter values.
part2CountBits:
	mov	X3, #1
	mov	X0, X21			// Put the number of bits into X0.
	sub	X0, X0, #1
	lsl	X3, X3, X0		// Our bit testing mask now has a 1 in the high bit position.
	mov	X1, #0			// Initialize loop variable for bit testing.

	// do while X1 < X21 and number of valid values > 1 count bits.
countNextBit:
	mov	X2, #0			// Initialize loop variable for value testing.
	mov	X7, #0			// Initialize bit count.
	// do while X2 < X4 process next value
countBitInNextValue:
	ldr	W0, [X5, X2, lsl #2]	// Load the value.
	tst	X0, X3			// Test this bit.
	cinc	X7, X7, ne		// If set, increment counter.
	add	X2, X2, #1		// Increment the loop counter.
	cmp	X2, X4			// Is this the last value?
	b.lo	countBitInNextValue	// No, process the next value.

	// We have counted the bits. Which bit we want depends on which pass we're on.
	lsl	X7, X7, #1		// Multiply the count by 2.
	// If the pass flag is zero, it means we're on the second pass.
	cbz	X11, pass2BitToUse

pass1BitToUse:
	// In pass 1 we use the more common bit and use 1 if the counts are equal.
	cmp	X7, X4			// Is it more than the number of values?
	cset	X8, hs			// Set X8 if so.
	b	startFilterValue

pass2BitToUse:
	// In pass 2 we use the less common bit and use 0 if the counts are equal.
	cmp	X7, X4			// Is the 1 count less than half the number of values?
	cset	X8, lo			// Set X8 if so.

startFilterValue:
	// Now filter the values that don't meet the criterion.
	mov	X2, #0			// Initialize loop variable for value testing.
	// do while X2 < X4 filter next value
filterValues:
	ldr	W0, [X5, X2, lsl #2]	// Load the value.
	cbz	X8, testForZero
testForOne:
	// Test to see if the bit is set. If so, we keep this value.
	tst	X0, X3			// Is the bit set?
	b.ne	keepValue		// Yes, keep this value.
	b	removeValue		// No, remove this value from the list.
testForZero:
	// Test to see if the bit is not set. If so, we keep this value.
	tst	X0, X3			// Is the bit set?
	b.eq	keepValue		// No, keep this value.
					// Yes, continue on to removeValue.
removeValue:
	mov	X9, X2			// Set the index to copy to.
	add	X10, X2, #1		// Set the index to copy from.
moveNextValue:
	cmp	X10, X4			// Are we finished copying values?
	b.hs	finishedRemovingValue
	ldr	W0, [X5, X10, lsl #2]	// Load the next value.
	str	W0, [X5, X9, lsl #2]	// Store it into this position.
	mov	W9, W10			// Set destination index to next location.
	add	W10, W10, #1		// Increase source index.
	b moveNextValue

finishedRemovingValue:
	sub	X4, X4, #1		// Decrement the number of valid values.
	b	filterLoopEnd

keepValue:
	add	X2, X2, #1		// We're keeping this variable so increment the loop counter.
filterLoopEnd:
	cmp	X2, X4			// Is the loop finished?
	b.lo	filterValues

	// We've filtered out any non-candidate values.
	cmp	X4, #1			// Have we narrowed it down to one candidate?
	b.eq	foundCandidate

	// We haven't narrowed it down to a single candidate yet so we need to filter based on the next bit.
	lsr	X3, X3, #1		// Shift the test bit right.
	add	X1, X1, #1		// Increment the bit index.
	cmp	X1, X21			// Is this the last bit?
	b.lo	countNextBit

	// If we get here it means we ran out of bits before we found a candidate.
	printStr	"Error: no candidate found."
	b exit

foundCandidate:
	cbz	X11, finishedPass2	// If zero, we've finished the second pass.

					// We've finished the first pass.
	ldr	W12, [X5]		// The pass 1 value is the first value in the list.
	mov	X11, #0			// Set pass flag to 0.
	b	part2PassStart

finishedPass2:
	ldr	W13, [X5]		// The pass 2 value is the second value in the list.

	mul	X0, X12, X13		// Multiply the two pass values to get the solution.
	printVal	part2String, 0

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
