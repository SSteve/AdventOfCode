// Advent of Code 2020, Day 2
// TODO: Get better with stacks. Put number of valid passwords in a local stack variable.

// Registers:
// x0  - Scratch.
// x9  - File descriptor of open file. Not needed after file is closed.
// x17 - Holds the number 10 for multiplying while reading the line.
// w18 - Current character.
// x19 - End of input file.
// x20 - Current file position.
// x21 - Value 1.
// x22 - Value 2.
// w23 - Letter of interest.
// x24 - Pointer to string buffer for reading.
// x25 - Letter counter for Part 1 while reading line.
//     - Pointer into string buffer for Part 2.
// x26 - Number of valid passwords in Part 1.
// x27 - Number of valid passwords in Part 2.




#include <asm/unistd.h>
#include "fileio.S"
#include "armmacros.s"

.equ	BUFFERLEN,	24000

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

// Each input line:
//   ##-## c: string

nextLine:
	mov	x17, 10			// Store a 10 for mulitplication.
	mov	x21, 0			// Initialize Value 1.
	mov	x22, 0			// Initialize Value 2.
	mov	x25, 0			// Initialize count of letter of interest.
readValue1:
	ldrb	w18, [x20], 1		// Load the next character into w18.
	cmp	w18, '-'		// Is it a hyphen?
	b.eq	readValue2		// Yes, we're finished with the first value.
	mul	x21, x21, x17		// Decimal left shift.
	sub	w18, w18, '0'		// Convert ASCII to binary.
	add	x21, x21, w18, SXTB	// Add digit to value.
	b	readValue1

	// We've read Value 1 and the following hyphen. Now read Value 2.
readValue2:
	ldrb	w18, [x20], 1		// Load the next character into w18.
	cmp	w18, ' '		// Is it a space?
	b.eq	readLetter		// Yes, we're finished with the second value.
	mul	x22, x22, x17		// Decimal left shift.
	sub	w18, w18, '0'		// Convert ASCII to binary
	add	x22, x22, w18, SXTB	// Add digit to value.
	b	readValue2

readLetter:
	ldrb	w23, [x20], 3		// Load the letter of interest into w23 and
					//    skip the colon and space.

	ldr	x24, =string		// Load beginning of string buffer into x24.
readString:
	ldrb	w18, [x20], 1		// Load next character into w18.
	cmp	w18, '\n'		// Are we at the end of the line?
	b.eq	part1			// Yes, process this line.
	strb	w18, [x24], 1		// Not at the end of the line, so store this character.
	cmp	w18, w23		// Is this the same as the letter of interest?
	cinc	x25, x25, eq		// If so, increment the counter.
	cmp	x20, x19		// Are we at the end of the file?
	b.ge	part1			// Yes, process this line.
	b	readString		// Not finished with the line so get the next character.

part1:
	cmp	x25, x21		// Compare the letter count to the minimum value.
	cset	x0, ge			// If it's greater or equal, set x0
	cmp	x25, x22		// Compare the letter count to the maximum value.
	cset	x1, le			// If it's less or equal, set x1
	ands	xzr, x0, x1		// Are both tests true?
	cinc	x26, x26, ne		// If both true, increment the number of valid passports.

part2:
	sub	x21, x21, 1		// Subtract 1 from Value 1 and Value 2 to convert from
	sub	x22, x22, 1		//     1-based addressing to 0-based addressing
	ldr	x25, =string		// Load start of string buffer.
	ldrb	w18, [x25, x21]		// Load the character pointed to by Value 1.
	cmp	w18, w23		// Is this the same as the character of interest?
	cset	x0, eq			// If so, set x0.
	ldrb	w18, [x25, x22]		// Load the character pointed to by Value 2.
	cmp	w18, w23		// Is this the same as the character of interest?
	cset	x1, eq			// If so, set x1.
	cmp	x0, x1			// Are x0 and x1 the same?
	cinc	x27, x27, ne		// If they aren't the same, this is a valid passport.

part2Finished:
	cmp	x20, x19		// Are we at the end of the file?
	b.lt	nextLine		// Process the next line.

	printVal	part1String, 26
	printVal	part2String, 27

exit:
	mov	x0, 0			// Return code
	pop1	lr
	ret


.data
fileName:
	.asciz	"2.txt"
buffer:
	.fill	BUFFERLEN + 1, 1, 0
string:
	.fill	200, 1, 0
inputError:
	.asciz	"Failed to open input file.\n"
inputErrorLen:
	.word	. - inputError
part1String:
	.asciz "Part1: "
part2String:
	.asciz "Part2: "

