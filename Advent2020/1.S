// 
//
// Registers:

// While loading file:
// x0  - holds the number 10 for multiplying.
// x9  - input file descriptor.
// x10 - pointer to end of input buffer.
// x11 - current position in buffer.
// x12 - current value.
// w13 - current character.
// x24 - stack offset to next value.

// While finding values:
// x16 - outer loop offset.
// x17 - second loop offset.
// x18 - third loop offset.
// x19 - outer loop value.
// x20 - second loop value.
// x21 - third loop value.
// x22 - sum of loop values.
// x23 - temporary sum of outer two loop values.
// x24 - location past last value read.


#include <asm/unistd.h>
#include "fileio.S"
#include "armmacros.s"

.equ	BUFFERLEN,	2047
.equ	O_RDONLY,	0

.global	main

main:
	push1	lr
	sub	sp, sp, #2048		// Allocate 256 values on the stack.
	mov	x24, #0			// Initialize stack offset.
	
	openFile	fileName, O_RDONLY
	adds	x9, xzr, x0		// Save file descriptor.
	b.pl	openOk			// Positive value means file is open.
	mov	x1, #1			// stdout
	ldr	x2, =inputErrorLen	// Error message length.
	ldr	w2, [x2]
	writeFile	x1, inputError, x2	// Print the error message.
	b	exit

	// File opened successfully.
openOk:	
	// Read the entire file into the buffer.
	readFile	x9, buffer, BUFFERLEN
	ldr	x11, =buffer		// Start at beginning of buffer.
	add	x10, x11, x0		// End of buffer is buffer address plus
					//  x0 which contains the number of characters read.

	mov	x12, #0			// Initialize the current value
	mov	x0, #10			// Keep the number 10 for multiplying.
	b	skipNewlines

nextDigit:
	// We know w13 contains a digit.
	mul	x12, x12, x0		// Decimal left shift.
	sub	w13, w13, #'0'		// Convert from ascii to binary.
	add	x12, x12, w13, SXTB	// Add the new digit to the current value.
	cmp	x11, x10		// See if we're at the end of the file.
	b.ge	gotNumber		// If so, the file ended with a number and not a newline.
	ldrb	w13, [x11], #1		// Load the next character.
	cmp	w13, #'0'		// Compare it to ASCII 0.
	b.ge	nextDigit		// If it's >=, we're still working on a number.

gotNumber:
	str	x12, [sp, x24, lsl #3]	// Push the number on the stack.
	add	x24, x24, #1		// Increment the stack offset.
	mov	x12, #0			// Initialize the current value.

skipNewlines:
	cmp	x11, x10		// See if we're at the end of the file.
	b.ge	finishedLoading		// If so, we're done.

	// Read the next character in the buffer
	ldrb	w13, [x11], #1		// Load the next character into w13.
	cmp	w13, #'0'		// See if the character is less than ASCII 0.
	b.ge	nextDigit		// If so, it's a digit so get the next digit.
	b	skipNewlines		// If not, keep skipping any newlines.

finishedLoading:	
	flushClose	x9
	
	mov	x16, #0			// Initialize loop offset.
part1Loop1:
	ldr	x19, [sp, x16, lsl#3]	// Load the outer loop value.
	add	x17, x16, #1		// Initialize inner loop offset.
part1Loop2:
	ldr	x20, [sp, x17, lsl#3]	// Load the inner loop value.
	add	x22, x19, x20		// Add the two values.
	cmp	x22, #2020		// Compare to the target value.
	b.eq	foundPart1

	add	x17, x17, #1		// Increment inner loop offset.
	cmp	x17, x24		// Compare to end of list.
	b.lt	part1Loop2		// If we aren't at the end, continue the inner loop.
	// We've reached the end of the inner loop
	add	x16, x16, #1		// Increment outer loop offset.
	cmp	x16, x24		// Compare to end of list.
	b.lt	part1Loop1		// If we aren't at the end, continue the outer loop.

	// If we get here it means we found no answer.
	printStr	"No solution for part 1"
	b	part2

foundPart1:
	mul	x0, x19, x20
	printVal	part1String, 0

part2:
	mov	x16, #0
part2Loop1:
	ldr	x19, [sp, x16, lsl#3]	// Load the outer loop value.
	add	x17, x16, #1		// Initialize middle loop offset.
part2Loop2:
	ldr	x20, [sp, x17, lsl#3]	// Load the middle loop value.
	add	x23, x19, x20		// Sum of first two loops.
	add	x18, x17, #1		// Initialize inner loop offset.
part2Loop3:
	ldr	x21, [sp, x18, lsl#3]	// Load the inner loop value.
	add	x22, x21, x23		// Sum of all three loops.
	cmp	x22, #2020		// Compare to the target value.
	b.eq	foundPart2

	add	x18, x18, #1		// Increment inner loop offset.
	cmp	x18, x24		// Compare to end of list.
	b.lt	part2Loop3		// If we aren't at the end, continue the inner loop.
	// We've reached the end of the inner loop
	add	x17, x17, #1		// Increment middle loop offset.
	cmp	x17, x24		// Compare to end of list.
	b.lt	part2Loop2		// If we aren't at the end, continue the middle loop.
	// We've reached the end of the middle loop
	add	x16, x16, #1		// Increment outer loop offset.
	cmp	x16, x24		// Compare to end of list.
	b.lt	part2Loop1		// If we aren't at the end, continue the outer loop.

	// If we get here it means we found no answer.
	printStr	"No solution for part 2"
	b	exit

foundPart2:
	mul	x0, x19, x20		// Multiply the first two loop values.
	mul	x0, x0, x21		// Multiply by the inner loop value.
	printVal	part2String, 0

exit:
	mov	x0, #0			// Return code
	add	sp, sp, #2048
	pop1	lr
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

