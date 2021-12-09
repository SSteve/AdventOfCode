// Advent of Code 2020, Day 4
// Unfinished

// w18 - current character.
// x19 - end of input data.
// x20 - current file position.
// x21 - number of fields present in current passport.
// x22 - number of valid fields in current passport.

// x28 - number of valid passports for part 1.
// x29 - number of valid passports for part 2.

#include <asm/unistd.h>
#include "fileio.S"
#include "armmacros.s"

.equ	BUFFERLEN,	22000

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
	mov	x28, 0			// Initialize Part 1 answer.
	mov	x29, 0			// Initialize Part 2 answer.

readPassport:
	mov	x21, 0			// Initialize number of fields present in passport.
	mov	x22, 0			// Initialize number of valid fields in passport.

readField:
	// x0 is the base offset for the validation routines. We'll use x1 as the offset into
	// the jump table.
	// My goal here was to avoid branches by using lots of comparing and csel.
	adr	x0, validationRoutines	// Get the base address of the jump table.
	mov	x1, 0			// In case no correct field is found, we'll jump to an error message.
	ldrb	w18, [x20], 1		// Get next character.

	mov	x2, 1			// Offset for byr.
	cmp	w18, 'b'		// Is it 'b'?
	csel	x1, x2, x1, eq		// Load the offset for byr if it was 'b'.

	mov	x2, 2			// Offset for iyr.
	cmp	w18, 'i'		// Is it 'i'?
	csel	x1, x2, x1, eq		// Load the offset for iyr if it was 'i'.

	mov	x2, 3			// Offset for hgt.
	cmp	w18, 'h'		// Is it 'h'?
	b.ne	notH			// If not, skip to the next field. (Ok, one branch.)
	ldrb	w17, [x20]		// Look at the next character to decide between hgt & hcl.
	cmp	w17, 'c'		// Is it 'c'?
	cinc	x2, x2, eq		// If it's 'c', increase the offset.
	mov	x1, x2			// Load the offset for hgt or hct.
notH:
	mov	x2, 5			// Offset for eyr.
	cmp	w18, 'e'		// Is it 'e'?
	b.ne	notE			// If not, skip to the next field. (Ok, one more branch.)
	ldrb	w17, [x20]		// Look at the next character to decide between eyr & ecl.
	cmp	w17, 'c'		// Is it 'c'?
	cinc	x2, x2, eq		// If it's 'c', increase the offset.
	mov	x1, x2			// Load the offset for eyr or ecl.
notE:
	mov	x2, 7			// Offset for pid.
	cmp	w18, 'p'		// Is it 'p'?
	csel	x1, x2, x1, eq		// Load the offset for pid if it was 'p'.

	mov	x2, 8			// Offset for bypass field, because we ignore cid.
	cmp	w18, 'c'		// Is it 'c'?
	csel	x1, x2, x1, eq		// Load the offset for bypass field if it was 'c'.

	add	x20, x20, 3		// Skip over the second two characters for the field and the colon.
	add	x0, x0, x1, lsl 3	// Add the offset to the jump table base address.
	ldr	x0, [x0]

	// Jump to the validation subroutine.
	blr	x0

	// Return from validation.
	cmp	x20, x19		// Are we at the end of the file?
	b.ge	passportFinished	// Record the results for this passport.

	// bypassField read the whitespace character after the field. Peek at the next character.
	// If it isn't a newline, read the next field.
	ldrb	w18, [x20]
	cmp	w18, '\n'
	b.ne	readField
	// If the next character is a newline, advance our file position and fall
	// through to passportFinished.
	add	x20, x20, 1

passportFinished:
	cmp	x21, 7			// Did we find 7 fields?
	cinc	x28, x28, eq		// If so, increment part 1 answer.
	cmp	x22, 7			// Did we find 7 valid fields?
	cinc	x29, x29, eq		// If so, increment part 2 answer.

	cmp	x20, x19		// Are we at the end of the file?
	b.lt	readPassport		// If not, read the next passport.
					// If so, fall through to reportResults.

reportResults:
	printVal	part1String, 28
	printVal	part2String, 29

exit:
	mov	x0, 0			// Return code
	pop1	lr
	ret

// Read from input until space, cr, or eof
bypassField:
	cmp	x20, x19		// Are we at the end of the file?
	b.ge	bypassed		// If so, return.
	ldrb	w18, [x20], 1		// Read the next character.
	cmp	w18, ' '		// Is it a space?
	cset	x0, eq			// Yes, set up x0 for the ORR test.
	cmp	w18, '\n'		// Is it a newline?
	cinc	x0, x0, eq		// Yes, add 1 to x0.
	cmp	x0, 0			// Test if space or newline.
	b.ne	bypassField		// If not whitespace, continue eating characters.
bypassed:
	ret				// Return from validation.


validateByr:
	add	x21, x21, 1		// Add one to the number of fields present.
	push1	lr			// Push lr before calling subroutine.
	bl	readYear		// Read the year value.
	pop1	lr
	sub	x0, x0, 1920		// Offset by first valid year.
	cmp	x0, 2002 - 1920		// Compare to highest valid year.
	cinc	x22, x22, ls		// Increment valid passports if unsigned lower or same.
	b	bypassField

validateIyr:

validateHgt:

validateHcl:

validateEyr:

validateEcl:

validatePid:

unknownField:
	printStr	"Unknown field. Aborting."
	b	exit

readYear:
	mov	x2, 10			// A ten for decimal left shift.
	mov	x1, 4			// Read four digits. We know the input is always four digits.
	mov	x0, 0			// Return value.
readDigit:
	ldrb	w18, [x20], 1		// Get the next digit.
	sub	w18, w18, '0'		// Convert ASCII to binary.
	cmp	w18, 9			// Is this greater than 9?
	b.hi	bypassField		// Invalid character. Skip the rest of the field value.
	madd	x0, x0, x2, x18		// value = value * 10 + digit
	subs	x1, x1, 1		// Decrement loop counter.
	b.gt	readDigit
	ret


	.balign	8
validationRoutines:
	.quad	unknownField
	.quad	validateByr
	.quad	validateIyr
	.quad	validateHgt
	.quad	validateHcl
	.quad	validateEyr
	.quad	validateEcl
	.quad	validatePid
	.quad	bypassField

.data
	.align 4
fileName:
	.asciz	"4test.txt"
buffer:
	.fill	BUFFERLEN + 1, 1, 0
inputError:
	.asciz	"Failed to open input file.\n"
inputErrorLen:
	.word	. - inputError
part1String:
	.asciz	"Part1: "
part2String:
	.asciz	"Part2: "
