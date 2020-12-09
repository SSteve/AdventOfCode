// Advent of Code 2020, Day 3

// w18 - Current character.
// x19 - End of input file while reading data.
//     - Current column while processing data.
// x20 - Current file position while reading data.
//     - Number of rows left on this run.
// x21 - Number of trees per row.
// x22 - Number of columns per move.
// x23 - Number of rows per move.
// x24 - Pointer into trees data while reading. Points
//       to beginning of row. Add current column to offset
//       into trees data.
// x25 - Number of trees hit in this run.
// x26 - Part 2 puzzle answer.
// x27 - Pointer into slopes data.
// x28 - Number of rows in trees data.


#include <asm/unistd.h>
#include "fileio.S"
#include "armmacros.s"

.equ	BUFFERLEN,	12000

.global main

main:
	push1 lr

	openFile	fileName, O_RDONLY
	adds	x9, xzr, x0		// Save file descriptor.
	b.pl	openOk			// Positive value means file is open.
	mov	x1, 1			// stdout
	ldr	x2, =inputErrorLen	// Error message length.
	ldr	w2, [x2]
	writeFile	x1, inputError, x2	// Print the error message
	b	exit

	// File opened successfully.
openOk:
	// Read the entire file into the buffer.
	readFile	x9, buffer, BUFFERLEN

	ldr	x20, =buffer		// Set file position to beginning of buffer.
	add	x19, x20, x0		// Set end of file position. (x0 contains number of
					//    characters that were read.)
	flushClose	x9		// Close file after getting value from x0.

readFile:
	mov	x21, 0			// Initialize the number of trees per row.
	mov	x28, 0			// Initialize the number of rows.
	ldr	x24, =trees		// Ge// Keep a zero and one for storing the tree values.t the pointer to the trees data.
readFirstLine:
	ldrb	w18, [x20], 1		// Load next character from file data.
	cmp	w18, '\n'		// Is it the end of the line?
	cinc	x28, x28, eq		// Increment number of lines if end of the line.
	b.eq	readSubsequentLines	// Finished with the first line.
	cmp	w18, '.'		// Is it an empty cell?
	cset	w18, ne			// Store 0 or 1 as required.
	strb	w18, [x24], 1		// Store the value into the trees data.
	add	x21, x21, 1		// Increment the number of trees per row.
	b	readFirstLine

readSubsequentLines:
	ldrb	w18, [x20], 1		// Load next character from file data.
	cmp	w18, '\n'		// Is it the end of the line?
	cinc	x28, x28, eq		// Increment number of lines if end of the line.
	b.eq	skipNewline		// Don't store newlines.
	cmp	w18, '.'		// Is it an empty cell?
	cset	w18, ne			// Store 0 or 1 as required.
	strb	w18, [x24], 1		// Store the value into the trees data.
skipNewline:
	cmp	x20, x19		// Are we at the end of the file?
	b.lt	readSubsequentLines

	add	x28, x28, 1		// Increment number of lines when we hit the end of the file.

finishedReadingFile:
	mov	x26, 1			// Initialize puzzle answer. We'll be multiplying
					//    values into the register.
	ldr	x27, =slopes		// Initialize pointer into slopes data.

takeNextRun:
	ldr	x24, =trees		// Initialize pointer into trees data.
	mov	x19, 0			// Initialize current column.
	mov	x20, x28		// Initialize number of rows to process.
	ldr	x0, =endOfSlopes
	cmp	x27, x0			// Have we processed the last slope?
	b.ge	finished		// Yes, show the answers.
	ldp	x22, x23, [x27], 16	// Load number of columns and rows per move.
	mov	x25, 0			// Number of trees hit in this run.

nextRow:
	ldrb	w18, [x24, x19]		// Load the cell.
	add	x25, x25, w18, SXTB	// Add the cell to the number of trees hit.
	mul	x0, x21, x23		// Multiply the number of trees per row by the number
					//   of rows per move.
	add	x24, x24, x0		// Add to the pointer into tree data.
	add	x19, x19, x22		// Add number of columns to current column.
	cmp	x19, x21		// Are we past the end of the row?
	csel	x0, x21, xzr, ge	// If so, load number of trees per row into x0.
	sub	x19, x19, x0		// Subtract number of trees per row if we're past end of row.
	subs	x20, x20, x23		// Decrement number of rows.
	b.gt	nextRow			// If number of rows to process is > 0, do next row.

	// Finished with run
	mul	x26, x26, x25		// Multiply the number of trees hit into the puzzle answer.
	b	takeNextRun		// Do the next run.



finished:
	printVal	part1String, 25
	printVal	part2String, 26

exit:
	mov	x0, 0			// Return code
	pop1	lr
	ret


.data
fileName:
	.asciz	"3.txt"
buffer:
	.fill	BUFFERLEN + 1, 1, 0
trees:
	.fill	BUFFERLEN, 1, 0
inputError:
	.asciz	"Failed to open input file.\n"
inputErrorLen:
	.word	. - inputError
part1String:
	.asciz	"Part1: "
part2String:
	.asciz	"Part2: "
	.align 4
slopes:
	.quad	1, 1, 5, 1, 7, 1, 1, 2, 3, 1
endOfSlopes:

