// Advent of Code 2021 Day 5
// Included files are at https://github.com/SSteve/AdventOfCode/tree/master/Advent2021

.nolist
#include <asm/unistd.h>
#include "fileio.S"
#include "armmacros.s"
#include "armutilities.s"
.list

// The buffer for reading the input file.
	.equ	BUFFER_SIZE,	10000

// The list pointer contains the pointer to the head of the list.
	.equ	list_head, 0
	.equ	list_size, 8		// The list head is a 64-bit pointer

// The node for storing the count at each coordinate.
	.equ	node_coord, 0		// The x and y values packed into a single 64-byte value.
	.equ	node_coord_x, 0		// The 32-bit X value of the coordinate.
	.equ	node_coord_y, 4		// The 32-bit Y value of the coordinate.
	.equ	node_count, 8		// The count at this coordinate.
	.equ	node_next, 16		// Pointer to the next node in the list.
	.equ	node_size, 24		// Total size of each node.

.global	main

////////////////////////////////////////////////////////
// Free all the storage associated with the diagram.
////////////////////////////////////////////////////////
// Input:
//   X0 - Pointer to the list head.
// Output:
//   None
// Registers:
//   X19 - Address of next node.
freeNodes:
	push2	X19, LR
	ldr	X19, [X0, #list_head]	// Copy list head to X19.
freeNodes_next:
	cbz	X19, freeNodes_done
	mov	X0, X19
	ldr	X19, [X19, #node_next]
	bl	free
	b	freeNodes_next

freeNodes_done:
	pop2	X19, LR
	ret

////////////////////////////////////////////////////////
// Look up the given coordinate.
// If the coordinate is in the list, return a pointer
// to the coordinate's node.
// If the coordinate is not in the list, return a pointer
// to the node after which the coordinate should be inserted.
// If the insertion point is the head of the list, return NULL.
////////////////////////////////////////////////////////
// Input:
//   X0 - Pointer to first node in list.
//   X1 - Coordinate.
// Output:
//   X0 - Pointer to the coordinate or the node it should
//        be inserted before.
// Registers used:
//   X2 - Pointer to previous node.
//   X3 - Coordinate at current node.
lookup:
	mov	X2, #0			// Set previous pointer to NULL.
lookup_next:
	cbz	X0, lookup_stop		// If the pointer to the current node is NULL,
					//   stop looking.
	ldr	X3, [X0, #node_coord]	// Load the coordinate at the current node.
	cmp	X3, X1			// Is the coordinate greater than or equal to
					//   the one we're looking for?
	b.eq	lookup_exit		// If it's equal, we've found the coordinate, so
					//   return the pointer to this node.
	b.hi	lookup_return_previous	// If it's higher, return the pointer to the previous node.
	mov	X2, X0			// previous = current.
	ldr	X0, [X0, #node_next]	// current = current->next.
	b	lookup_next
lookup_stop:
	cmp	X0, #0			// If the pointer to the current node is NULL,
	b.eq	lookup_return_previous	//   return the pointer to the previous node.
	b	lookup_exit		// Else return the pointer to the current node.
lookup_return_previous:
	mov	X0, X2
lookup_exit:
	ret



////////////////////////////////////////////////////////
// Increment the node count at the given coordinate.
////////////////////////////////////////////////////////
// Input:
//   X0 - Pointer to the structure that holds the head of the list of coordinates.
//   X1 - Coordinate.
// Registers used:
//   X2 - Pointer to new (or found) node.
//   X3 - Count at node returned from lookup.
//   X4 - Scratch.
//   X19 - Copy of input X0.
//   X20 - Copy of input X1.
incrementCoordinate:
	push1	LR
	push2	X19, X20
	mov	X19, X0
	mov	X20, X1
	ldr	X0, [X0, #list_head]
	bl	lookup
	cbz	X0, createNewNode	// A new node needs to be at the beginning
					//   of the list, so create a new node.
	ldr	X3, [X0, #node_count]	// Load the count at the current node
	ldr	X4, [X0, #node_coord]	// Load the coordinate returned by lookup.
	cmp	X4, X20 		// Is it the coordinate we're incrementing?
	csel	X2, X0, X2, eq		// Yes, point X2 to the found node.
	b.eq	perform_increment	// Yes, increment the count at this node.
createNewNode:
	// The node doesn't exist in the list so we need to create a new one.
	push2	X0, X1			// Save pointer to the node and the coordinate value.
	mov	X0, #node_size		// We want to allocate memory for one node.
	bl	malloc
	mov	X2, X0			// Copy the pointer to the new node to X2.
	pop2	X0, X1			// Restore the node and the coordinate value.
	mov	X3, #0			// Initialize the count to zero.
	str	X20, [X2, #node_coord]	// Store the coordinate value in the new node.
	cbz	X0, insertAtHead	// Are we inserting at the beginning of the list?
	ldr	X4, [X0, #node_next]	// No. Load the pointer to the next node.
	str	X4, [X2, #node_next]	// And store it in the new node.
	str	X2, [X0, #node_next]    // Point the previous node at this one.
	b	perform_increment
insertAtHead:
	// The search returned NULL, so the new node is now at the head of the list.
	ldr	X4, [X19, #list_head]	// Load the pointer to the head of the list.
	str	X4, [X2, #node_next]	// Make this node point to the previous head of the list.
	str	X2, [X19, #list_head]	// Point the head of the list at this node.

perform_increment:
	add	X3, X3, #1		// Increment the value.
	str	X3, [X2, #node_count]   // Write it to the node.
increment_done:
	pop2	X19, X20
	pop1	LR
	ret

////////////////////////////////////////////////////////
// Create a vertical line
// Increment count at each coordinate from (x1, y1)
// to (x2, y2). We know that x1 and x2 are equal.
////////////////////////////////////////////////////////
// Input:
//   X0 - Pointer to head of list.
//   W1 - x1
//   W2 - y1
//   W3 - x2
//   W4 - y2
// Output:
//   None
// Registers used:
//   X19 - Pointer to head of list.
//   W20 - x value.
//   W21 - current, lower y value.
//   W22 - higher y value.
createVerticalLine:
	push2	LR, X19
	push2	X20, X21
	push2	X22, X23
	mov	X19, X0
	mov	W20, W1
	cmp	W2, W4			// See if first y value is lower than second.
	csel	W21, W2, W4, lo		// W21 = min(W2, W4)
	csel	W22, W2, W4, hi		// W22 = max(W2, W4)
cvlNextPoint:
	mov	X0, X19			// Pointer to head of list is first argument.
	lsl	X1, X20, #32		// Put x value in coordinate.
	orr	X1, X1, X21		// Add the y value.
	bl	incrementCoordinate
	add	W21, W21, #1		// Increment current y value
	cmp	W21, W22		// Are we finished?
	b.ls	cvlNextPoint		// No, keep going.

	pop2	X22, X23
	pop2	X20, X21
	pop2	LR, X19
	ret


////////////////////////////////////////////////////////
// Create a horizontal line
// Increment count at each coordinate from (x1, y1)
// to (x2, y2). We know that y1 and y2 are equal.
////////////////////////////////////////////////////////
// Input:
//   X0 - Pointer to head of list.
//   W1 - x1
//   W2 - y1
//   W3 - x2
//   W4 - y2
// Output:
//   None
// Registers used:
//   X19 - Pointer to head of list.
//   W20 - y value.
//   W21 - current, lower x value.
//   W22 - ending x value.
createHorizontalLine:
	push2	LR, X19
	push2	X20, X21
	push2	X22, X23
	mov	X19, X0
	mov	W20, W2
	cmp	W1, W3			// See if first x value is lower than second
	csel	W21, W1, W3, lo		// W21 = min(W1, W3)
	csel	W22, W1, W3, hi		// W22 = max(W1, W3)
chlNextPoint:
	mov	X0, X19			// Pointer to head of list is first argument.
	lsl	X1, X21, #32		// Put x value in coordinate.
	orr	X1, X1, X20		// Add the y value.
	bl	incrementCoordinate
	add	W21, W21, #1		// Increment current x value
	cmp	W21, W22		// Are we finished?
	b.ls	chlNextPoint		// No, keep going.

	pop2	X22, X23
	pop2	X20, X21
	pop2	LR, X19
	ret


////////////////////////////////////////////////////////
// Calculate count for part 1. It is the number of points
// where the count is at least two.
////////////////////////////////////////////////////////
// Input:
//   X0 - Pointer to head of list.
// Output:
//   X0 - Number of points where count is at least two.
// Registers used:
//   X1 - Pointer to current node.
//   X2 - Count at current node.
countPart1:
	ldr	X1, [X0, #list_head]	// Load pointer to first node.
	mov	X0, #0			// Initialize count.
cp1Next:
	cbz	X1, cp1Done		// If the pointer is null, we're done.
	ldr	X2, [X1, #node_count]	// Load the count at this node.
	cmp	X2, #2			// Is it >= 2?
	cinc	X0, X0, hs		// Yes, increment count.
	ldr	X1, [X1, #node_next]	// Load the pointer to the next node.
	b	cp1Next
cp1Done:
	ret

////////////////////////////////////////////////////////
// Main
////////////////////////////////////////////////////////
// Registers:
//   While reading file:
//     X19 - Current file buffer location.
//     X20 - Address of first byte after file buffer.
//     X21 - Address of coordinate value.
//     X23 - Number of lines in file.
//     X26 - Loop counter for reading values.
//     X28 - Pointer to memory allocated for storing coordinates.
//     FP (X29)  - Pointer to file buffer.
//   After reading file:
//     X19 - Loop counter for processing line segments.
//     X21 - Address of next line segment value.
//     X23 - Number of lines read. Each line is x1,y1 -> x2,y2 and are 32-bit values.
//     X28 - Pointer to memory allocated for storing coordinates.
//     FP (X29) - Pointer to structure that points to the head of the list.
// Stack:
//   Address of memory allocated for coordinate values.
main:
	push2	LR, FP

	// Allocate memory for reading the file.
 	mov	X0, #BUFFER_SIZE
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
	b	exitAfterFreeingCoordinateMemory

	// File opened successfully.
openOk:
	// Load the file into the allocated memory.
	readFileDynamic	X9, FP, BUFFER_SIZE
	mov	X19, FP			// Put beginning of buffer into X19.
	add	X20, X19, X0		// End of buffer is buffer address plus
					//  X0 which contains the number of characters read.
	flushclose X9

// Count the number of lines in the file. We'll use this to determine how much memory to allocate
// for the coordinate data.
	mov	X23, #0			// Initialize number of lines in the file.
lookForNewLines:
	ldrb	W0, [X19], #1		// Read the next character in the file.
	cmp	W0, #'\n'		// Is it a newline?
	cinc	X23, X23, eq		// If yes, increment line count.
	cmp	X19, X20		// Are we at the end of the buffer?
	b.lo	lookForNewLines		// No, keep looking.

	// Check to see if last character is a newline. If not, increment the number of lines in the file.
	sub	X19, X20, #1		// Point to last character in file buffer.
	ldrb	W0, [X19]		// Get the last character.
	cmp	W0, #'\n'		// Is it a newline?
	cinc	X23, X23, ne		// If not, increment line count.

// Allocate memory for coordinate values
	lsl	X0, X23, #4		// Each line of coordinates takes 16 bytes so multiply
	bl	malloc			// the line count by 16 to calculate how much memory to allocate.
	push1	X0			// Push the address of allocated memory onto the stack.
	mov	X28, X0			// Copy the address to X28.

// Store the values from the file into memory.
	mov	X21, X28		// Initialize pointer to next coordinate value.
	mov	X19, FP			// Set current buffer location back to beginning of file data.
	lsl	X26, X23, #2		// Initialize loop counter for reading lines. There are four values
					// per line so multiply the line count by 4 to get the number of
					// values to read.
readNextValue:
	// Read the x and y values for the start and end of each line.
	mov	X0, X19			// Current buffer location is first argument to loadDecimalValue.
	mov	X1, X20			// End of buffer is second argument to loadDecimalValue.
	bl	loadDecimalValue
	mov	X19, X1			// Update the current buffer location.
	str	W0, [X21], #4		// Store coordinate value and point to next word.
	sub	X26, X26, #1		// Decrement value-reading loop counter.
	cbnz	X26, readNextValue	// If loop isn't zero, read the next value.

fileIsLoaded:
	// We've finished reading the file so free the allocated memory.
	mov	X0, FP			// Copy address of allocated memory to input argument.
	bl	free			// Free the allocated memory that held the input file.

// Create the head pointing to the list of nodes.
	mov	X0, #list_size		// We need to allocate the structure that holds the pointer to the list head.
	bl	malloc
	mov	FP, X0			// Store the pointer to the allocated memory.
	str	XZR, [FP, #list_head]	// Set the list head to NULL.

// Create straight lines.
	mov	X21, X28		// Initialize pointer to first coordinate value.
	mov	X19, X23		// Initialize loop counter.
createNextStraightLine:
	mov	X0, FP			// Load pointer to list head
	ldr	W1, [X21], #4		// Load x1
	ldr	W2, [X21], #4		// Load y1
	ldr	W3, [X21], #4		// Load x2
	ldr	W4, [X21], #4		// Load y2
	cmp	W1, W3			// Is this a vertical line?
	b.ne	isLineHorizontal
	bl	createVerticalLine
	b	straightLineLoopDone

isLineHorizontal:
	cmp	W2, W4			// Is this a horizontal line?
	b.ne	straightLineLoopDone
	bl	createHorizontalLine

straightLineLoopDone:
	subs	X19, X19, #1		// Decrement loop counter.
	b.ne	createNextStraightLine	// Create lines until loop counter is zero.

part1:
	mov	X0, FP			// Load pointer to list head
	bl	countPart1

	printVal	part1String, 0

exit:
	// Free the diagram.
	mov	X0, FP			// Copy the list head structure to X0.
	bl	freeNodes
	mov	X0, FP			// Copy the list head structure to X0.
	bl	free			// Free the memory allocated for the list head structure.

	// Free the memory allocated for coordinate values.
	pop1	X0
	bl	free

exitAfterFreeingCoordinateMemory:
	pop2	LR, FP
	mov	X0, #0			// Return code
	ret

.data
fileName:
	.asciz	"5.txt"
//	.asciz	"5test.txt"
	.align	4

drawnNumbers:
	.space	512

boards:
	.space	100
	.align	4

inputError:
	.asciz	"Failed to open input file.\n"
inputErrorLen:
	.word	. - inputError
part1String:
	.asciz "Part1: "
part2String:
	.asciz "Part2: "
