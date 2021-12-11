// Advent of Code 2021 Day 4
// Included files are at https://github.com/SSteve/AdventOfCode/tree/master/Advent2021

#include <asm/unistd.h>
#include "fileio.S"
#include "armmacros.s"
#include "armutilities.s"

.equ	boardSize,	26
.equ	NUMBERS_PER_BOARD,	25
// The first byte of the bingo board is the boardHasBingo flag which means a bingo was
// already found on that board. The following 25 bytes are the values on the board.

.equ	BUFFER_SIZE,	8192

.global	main

////////////////////////////////////////////////////////
// Apply Number to Board
////////////////////////////////////////////////////////
// If the board contains the drawn number, replace the number on the board with the
// sentinel 0xFF. If the board already has a bingo, return right away because we
// don't need to process it any more.
// Input:
//   W0 - Number drawn.
//   X1 - Starting address of board.
// Output:
//   No return value.
// Registers used:
//   W2 - Number read from board.
//   X3 - Loop counter for processing numbers.
//   W4 - 0xFF to write to number that has been drawn.
applyNumberToBoard:
	mov	W4, #-1			// Load sentinel value into W4
	ldrb	W2, [X1], #1		// Load boardHasBingoFlag and increment pointer.
	cbnz	W2, antbDone		// If non-zero, this board already has a bingo so we can skip it.
	mov	X3, #NUMBERS_PER_BOARD	// Initialize loop counter.
antbNextNumber:
	// Process the next bingo board number.
	ldrb	W2, [X1], #1		// Get next board number and increment pointer.
	cmp	W2, W0			// Is it the number drawn?
	b.eq	antbNumberFound		// Yes, mark the number and exit loop.
	sub	X3, X3, #1		// Decrement loop counter.
	cbnz	X3, antbNextNumber	// Still more numbers to process.
	b	antbDone		// This board doesn't contain the drawn number, so exit subroutine.

antbNumberFound:
	strb	W4, [X1, #-1]		// Write the sentinel value to the matching number.

antbDone:
	ret

////////////////////////////////////////////////////////
// Look for a marked row on a bingo card
////////////////////////////////////////////////////////
// Input:
//   X0 - Address of row.
// Output:
//   X0 - Zero if row isn't marked, non-zero if it is.
// Registers used:
//   W2 - Number read from board.
//   X3 - Loop counter.
//   X4 - Current address.
lookForMarkedRow:
	mov	X4, X0			// Copy row address to X4
	mov	X0, #0			// Initialize return value.
	mov	X3, #5			// Set loop counter to 5.
checkNextRowValue:
	ldrb	W2, [X4], #1		// Load next value in row.
	cmp	W2, #0xFF		// Is this square marked?
	b.ne	lfmrDone		// No, this row isn't a bingo.
	sub	X3, X3, #1		// Decrement loop counter.
	cbnz	X3, checkNextRowValue	// If not zero, keep checking.
	// If we got here, it means this row has a bingo.
	mov	X0, #0xFF		// Set the return flag.
lfmrDone:
	ret

////////////////////////////////////////////////////////
// Look for a marked column on a bingo card
////////////////////////////////////////////////////////
// Input:
//   X0 - Address of first number in column.
// Output:
//   X0 - Zero if row isn't marked, non-zero if it is.
// Registers used:
//   W2 - Number read from board.
//   X3 - Loop counter.
//   X4 - Current address.
lookForMarkedColumn:
	mov	X4, X0			// Copy column address to X4
	mov	X0, #0			// Initialize return value.
	mov	X3, #5			// Initialize loop counter.
checkNextColValue:
	ldrb	W2, [X4], #5		// Load next value in column. Increment by 5 to point
					// to next value in column.
	cmp	W2, #0xFF		// Is this square marked?
	b.ne	lfmrDone		// No, this row isn't a bingo.
	sub	X3, X3, #1		// Decrement loop counter.
	cbnz	X3, checkNextColValue	// If not zero, keep checking.
	// If we got here, it means this column has a bingo.
	mov	X0, #0xFF		// Set the return flag.
lfmcDone:
	ret


////////////////////////////////////////////////////////
// Look for a bingo on this board
////////////////////////////////////////////////////////
// Examine the given board to see if it has a bingo. If a bingo was already found on this
// board, return immediately.
// Input:
//   X0 - Address of board to test.
// Output:
//   X0 - Zero if no bingo or was already a bingo. Non-zero if a new bingo.
// Registers used:
//   W2 - Number read from board.
//   X3 - Loop counter for processing numbers.
//   X4 - Beginning board address.
//   X5 - Pointer to current location in board.
lookForBingo:
	push1	LR
	mov	X4, X0			// Copy board address to X4. We must remember the
					// beginning of the board in case we need to change
					// the value of boardHasBingo.
	mov	X5, X0			// Initialize pointer into board.
	mov	X0, #0			// Clear the return flag.
	ldrb	W2, [X5], #1		// Load the boardHasBingo value.
	cbnz	W2, ldbExit		// If non-zero, we don't need to look for bingo on this board.

	// Look for bingo in rows.
	mov	X3, #5			// Initialize loop counter.
checkNextRow:
	mov	X0, X5			// The argument to lookedForMarkedRow is the address of the current row.
	push2	X3, X4
	push1	X5
	bl	lookForMarkedRow
	pop1	X5
	pop2	X3, X4
	cbnz	X0, lfbDone		// If X0 is non-zero, we found a bingo in this row.
	add	X5, X5, #5		// Increase pointer by 5 to point to next row.
	sub	X3, X3, #1		// Decrement loop counter.
	cbnz	X3, checkNextRow

	// We didn't find bingo in a row, so check columns.
	mov	X3, #5			// Initialize loop counter.
	add	X5, X4, #1		// Point to first number in column one.
checkNextColumn:
	mov	X0, X5			// The argument to lookForMarkedColumn is the address of the current column.
	push2	X3, X4
	push1	X5
	bl	lookForMarkedColumn
	pop1	X5
	pop2	X3, X4
	cbnz	X0, lfbDone		// If X0 is non-zero, we found a bingo in this row.
	add	X5, X5, #1		// Increase pointer by 1 to point to next column.
	sub	X3, X3, #1		// Decrement loop counter.
	cbnz	X3, checkNextColumn

lfbDone:
	strb	W0, [X4]		// X0 will be non-zero if bingo was found on this board.

ldbExit:
	pop1	LR
	ret


////////////////////////////////////////////////////////
// Calculate board score
////////////////////////////////////////////////////////
// The board score is the sum of all the unmarked numbers
// times the number that was just called.
// Input:
//   X0 - Pointer to board.
//   X1 - Last number drawn.
// Output:
//   X0 - Board score.
// Registers used:
//   W2 - Number read from board.
//   X3 - Loop counter for processing numbers.
//   X4 - Pointer to current location in board.
calculateBoardScore:
	add	X4, X0, #1		// Set pointer to first value on board (past boardHasBingo).
	mov	X0, #0			// Initialize return value.
	mov	X3, #NUMBERS_PER_BOARD	// Initialize loop counter.
cbsNextNumber:
	ldrb	W2, [X4], #1		// Load the next value.
	cmp	W2, #0xFF		// Is the number marked?
	b.eq	numberMarked		// Yes, don't include it in the sum.
	add	X0, X0, X2		// Add this number to the sum.
numberMarked:
	sub	X3, X3, #1		// Decrement loop counter.
	cbnz	X3, cbsNextNumber

	mul	X0, X0, X1		// Multiply sum by last number drawn.
	ret

////////////////////////////////////////////////////////
// Main
////////////////////////////////////////////////////////
// Registers:
//   While reading file:
//     X19 - Current file buffer location.
//     X20 - Address of first byte after file buffer.
//     X27 - Loop counter for reading bingo boards.
//     X28 - Pointer into bingo board memory.
//     FP  - Pointer to memory allocated with malloc.
//   After reading file:
//     W19 - Bingo number drawn.
//     X20 - Loop counter for processing bingo boards.
//     X21 - Pointer to next bingo number to draw.
//     X22 - Number of boards with a bingo.
//     X23 - Number of bingo boards read.
//     X24 - Pointer to next bingo card to process.
//     X25 - Part 1 solution.
//     X26 - Part 2 solution.
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
	b	exit

	// File opened successfully.
openOk:
	// Load the file into the allocated memory.
	readFileDynamic	X9, FP, BUFFER_SIZE
	mov	X19, FP			// Put beginning of buffer into X19.
	add	X20, X19, X0		// End of buffer is buffer address plus
					//  X0 which contains the number of characters read.


	flushclose X9

readFileData:
	ldr	X21, =drawnNumbers	// Load pointer to first drawn number.
	mov	X0, X19			// Copy beginning of buffer to loadDecimalValue input argument.

	// Read the drawn numbers. When the character at the input buffer location is
	// a carriage return, we've reached the end of the list.
readNextDrawnNumber:
	mov	X1, X20			// Copy end of buffer address to X1.
					// X0 already has the current buffer address.
	bl	loadDecimalValue
	strb	W0, [X21], #1		// Store the value into the list of drawn numbers and increment pointer.
	ldrb	W0, [X1]		// Load the character at the current buffer position.
	cmp	W0, #'\n'		// Is it a carriage return?
	b.eq	finishedDrawnNumbers
	mov	X0, X1			// Copy current buffer location to loadDecimalValue input argument.
	b	readNextDrawnNumber

finishedDrawnNumbers:
	mov	X19, X1			// Update current buffer location.
	mov	W0, #0xFF		// Load X0 with sentinel value.
	strb	W0, [X21]		// Store the sentinel value into the list of drawn numbers.

	mov	X23, #0			// Initialize number of bingo boards read.
	ldr	X28, =boards		// Load pointer to bingo boards.

readBingoBoard:
	strb	WZR, [X28], #1		// Initialize board.boardHasBingo to 0.
	mov	X27, #NUMBERS_PER_BOARD	// Set X27 to the count of numbers on each bingo board.
	mov	X0, X19			// Copy beginning of buffer to loadDecimalValue input argument.
readNextBoardNumber:
	mov	X1, X20			// Copy end of buffer address to X1.
					// X0 already has the current buffer address.
	bl	loadDecimalValue
	cmp	X0, #-1			// If no number was read, we've finished loading boards.
	b.eq	fileIsLoaded
	strb	W0, [X28], #1		// Copy loaded value into bingo board.
	mov	X0, X1			// Copy current buffer location to loadDecimalValue input argument.
	subs	X27, X27, #1		// Decrement loop counter.
	b.ne	readNextBoardNumber
	// Finished reading a bingo board.
	mov	X19, X1			// Update current buffer location.
	add	X23, X23, #1		// Increment bingo board count.
	b	readBingoBoard

fileIsLoaded:
	// We've finished reading the file so free the allocated memory.
	mov	X0, FP			// Copy address of allocated memory to input argument.
	bl	free			// Free the allocated memory.

	ldr	X21, =drawnNumbers	// Point X21 to the first number to draw.
drawNextNumber:
	ldrb	W19, [X21], #1		// Draw the next number and increment pointer.
	cmp	W19, #0xFF		// Have we reached the end without finding the solution?
	b.eq	dataError		// Yes, error.

	mov	X20, X23		// Initialize bingo board loop counter.
	ldr	X24, =boards		// Point X24 to the first bingo board.
applyNumberToNextBoard:
	mov	W0, W19			// Drawn number is first argument to applyNumberToBoard.
	mov	X1, X24			// Board address is second argument to applyNumberToBoard.
	bl	applyNumberToBoard
	add	X24, X24, #boardSize	// Point to next bingo board.
	sub	X20, X20, #1		// Decrement loop counter.
	cbnz	X20, applyNumberToNextBoard	// Apply the drawn number to the next bingo board.

	// We've applied the drawn number to all the boards. Now look for boards with a bingo.
	mov	X20, X23		// Initialize bingo board loop counter.
	ldr	X24, =boards		// Set bingo board pointer to first board.
lookForNextBingo:
	mov	X0, X24			// Board address is first argument to lookForBingo.
	bl	lookForBingo
	cbz	X0, nextBingoLoopEnd	// If X0 is 0, we didn't find a new bingo on this board.

	// If we get here, it means we found a bingo.
	add	X22, X22, #1		// Increment the number of boards with a bingo.
	cmp	X22, #1			// If this is the first board, the board's value is the answer to part 1.
	b.ne	isThisLastBingo

	mov	X0, X24			// The board pointer is the argument to calculateBoardScore.
	mov	W1, W19			// The last number drawn is the second argument to calculateBoardScore.
	bl	calculateBoardScore
	mov	X25, X0			// Copy the board value to X25.
	b	nextBingoLoopEnd	// Continue looking for bingos.

isThisLastBingo:
	cmp	X22, X23		// Is this the last board with a bingo?
	b.ne	nextBingoLoopEnd	// No, continue looking for bingos.

	mov	X0, X24			// The board pointer is the first argument to calculateBoardScore.
	mov	W1, W19			// The last number drawn is the second argument to calculateBoardScore.
	bl	calculateBoardScore
	mov	X26, X0			// Copy the board value to X26, the part 2 value.
	b	success			// We are done. Display the answer.

nextBingoLoopEnd:
	add	X24, X24, #boardSize	// Point to next bingo board.
	sub	X20, X20, #1		// Decrement loop counter.
	cbnz	X20, lookForNextBingo	// Look for bingo on the next bingo card.

	b	drawNextNumber		// We've processed all the cards so draw the next number.

dataError:
	printStr	"Reached the end of the data before a solution was found."
	b	exit

success:
	// Display answers to both parts.
	printVal	part1String, 25
	printVal	part2String, 26

exit:
	pop2	LR, FP
	mov	X0, #0			// Return code
	ret

.data
fileName:
	.asciz	"4.txt"
//	.asciz	"4test.txt"
	.align	4

drawnNumbers:
	.space	512

boards:
	.space	boardSize * 100
	.align	4

inputError:
	.asciz	"Failed to open input file.\n"
inputErrorLen:
	.word	. - inputError
part1String:
	.asciz "Part1: "
part2String:
	.asciz "Part2: "
