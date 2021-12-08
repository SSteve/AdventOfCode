.global loadBinaryValue

////////////////////////////////////////////////////////
// Load a value represented as a string of binary digits.
// Skips over invalid digits until a valid digit is found.
// Returns -1 if no valid value was found.
////////////////////////////////////////////////////////
loadBinaryValue:
// Input:
// X0 - pointer into buffer.
// X1 - pointer to end of buffer.
// Output:
// X0 - value loaded from buffer. -1 if no value was found.
// X1 - new position in buffer.
// Registers used:
// W2 - character loaded from buffer.
// X3 - value being built.
// X4 - flag for invalid digit.

	mov	X3, #-1		// Initialize result value.

lbvGetNextCharacter:
	cmp	X0, X1		// Are we at the end of the buffer?
	b.eq	lbvDone		// Yes, we are finished.

	ldrb	W2, [X0], #1	// Load next character and increment pointer.

	cmp	W2, #'0'	// Is this less than '0'?
	cset	X4, lo		// Yes, set invalid digit flag.
	cmp	W2, #'1'	// Is this greater than '1'?
	cinc	X4, X4, hi	// Yes, increment invalid digit flag.
	cbz	X4, lbvValidDigit	// If the flag is zero, this is a valid digit.

	// This isn't a valid digit. What we do depends on whether or not
	// we've previously had a valid digit.
	cmp	X3, #-1		// Have we started building the return value?
	b.ne	lbvDone		// Yes, so we've reached the end of binary digits and we're done.
	b	lbvGetNextCharacter	// We haven't found a valid character yet, so look at the next.

lbvValidDigit:
	// We have a valid digit character in W2.
	cmp	X3, #-1		// Have we started building the return value?
	csel	X3, XZR, X3, eq	// If not, set X3 to 0, otherwise don't change X3.
	sub	W2, W2, #'0'	// Convert ASCII to binary.
	lsl	X3, X3, #1	// Multiply X3 by 2.
	add	X3, X3, X2	// Add new digit.
	b lbvGetNextCharacter

lbvDone:
	mov	X1, X0		// Move buffer position into return register.
	mov	X0, X3		// Move our loaded value into the return register.
	ret