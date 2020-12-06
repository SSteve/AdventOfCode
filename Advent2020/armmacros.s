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

// Push all of the corruptable registers onto the stack.
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

// Pop all of the corruptable registers off of the stack.
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

// Print the contents of a register in decimal and hex.
// Pass the register number, not the full name.
.macro	printReg	regnum
	pushall
	mov	x2, X\regnum	// For the %d.
	mov	x3, X\regnum	// For the %x.
	mov	x1, #\regnum	// The register number for the %c.
	add	x1, x1, #'0'	// Convert the register number to ascii.
	ldr	x0, =printfStr	// The format string for printf.
	bl	printf		// Call printf.
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
// printf format string for printReg
printfStr:
	.asciz	"X%c = %32ld, 0x%016lx\n"
	.align	4
.text

