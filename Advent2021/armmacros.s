// Push one register onto the stack.
.macro	push1	reg
	str	\reg, [SP, #-16]!
.endm

// Pop one register off of the stack.
.macro	pop1	reg
	ldr	\reg, [SP], #16
.endm

// Push two registers onto the stack.
.macro	push2	reg1, reg2
	stp	\reg1, \reg2, [SP, #-16]!
.endm

// Pop two registers off of the stack.
.macro	pop2	reg1, reg2
	ldp	\reg1, \reg2, [SP], #16
.endm

// Push all of the corruptible registers onto the stack.
.macro	pushall
	push2	x0, x1
	push2	x2, x3
	push2	x4, x5
	push2	x6, x7
	push2	x8, x9
	push2	x10, x11
	push2	x12, x13
	push2	x14, x15
	push2	x16, x17
	push2	x18, lr
.endm

// Pop all of the corruptible registers off of the stack.
.macro	popall
	pop2	x18, lr
	pop2	x16, x17
	pop2	x14, x15
	pop2	x12, x13
	pop2	x10, x11
	pop2	x8, x9
	pop2	x6, x7
	pop2	x4, x5
	pop2	x2, x3
	pop2	x0, x1
.endm

// Read the next positive integer from the buffer.
// Input registers:
// X19 - Current input buffer location.
// X20 - Address of first byte after input buffer.
//
// Registers modified:
// X1  - Flag for invalid digit.
// X2  - The number 10 for multiplication.
// X3  - Next value read from buffer.
// Return register:
// X0  - If -1, no value was found.
.macro loadInteger
	mov	W2, #10		// Store a 10 for multiplication.
	mov	X0, #-1		// Initialize return value.

1:
	cmp	X20, X19
	b.eq	3f		// We're at the end of the buffer so stop.

	ldrb	W3, [X19], #1	// Load next character into W3 and
				//  increment pointer.
	cmp	W3, #'0'	// Is this less than '0'?
	cset	X1, lo		// Yes, set invalid digit flag.
	cmp	W3, #'9'	// Is this greater than '9'?
	cinc	X1, X1, hi	// Yes, increment invalid digit flag.
	cmp	X1, #0		// Is this a valid digit?
	b.eq	2f		// Yes, process digit.
	// This isn't a valid digit.
	cmp	X0, #-1		// Have we started building the return value?
	b.ne	3f		// Yes, so we've reached the end of the decimal digits and we're done.
	b	1b		// We haven't started building the value yet, so get the next character.
2:
	// Now we know we have a decimal digit.
	cmp	X0, #-1		// Have we started building the return value?
	csel	X0, XZR, X0, eq	// If not, set X0 to 0, otherwise don't change X0.
	sub	W3, W3, #'0'	// Convert ASCII to binary.
	umaddl	X0, W0, W2, X3	// Multiply return value by 10 and add new digit.
	b	1b		// Fetch next character.
3:
.endm


// Print the contents of a register in decimal and hex.
// Pass the register number, not the full name.
.macro	printReg	regnum
	pushall
	mov	x2, X\regnum	// For the %d.
	mov	x3, X\regnum	// For the %x.
	mov	x1, #\regnum	// The register number for the %c.
	//add	x1, x1, #'0'	// Convert the register number to ascii.
	ldr	x0, =printRegStr	// The format string for printf.
	bl	printf		// Call printf.
	popall
.endm

// Print a string and the value in a register.
.macro	printVal	str, regnum
	pushall
	mov	x2, X\regnum
	ldr	x1, =\str
	ldr	x0, =printValStr
	bl printf
	popall
.endm

// Print a string.
.macro	printStr	str
	pushall
	ldr	x0, =1f		// Load the string to print.
	bl	printf		// Call printf.
	popall
	b	2f		// Branch around the string.
1:	.asciz	"\str\n"
	.align	4		// Make sure we're properly aligned for instructions.
2:
.endm

.data
// printf format strings for macros
printRegStr:
	.asciz	"X%2d = %32ld, 0x%016lx\n"
printValStr:
	.asciz "%s%ld\n"
	.align	4
.text

