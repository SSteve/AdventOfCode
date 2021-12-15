	.equ	node_coord, #0
	.equ	node_count, #8
	.equ	node_left, #16
	.equ	node_right, #24
	.equ	node_height, #32
	.equ	node_size, #40

////////////////////////////////////////////////////////
// Set the height of the given node to the maximum of its
// left and right children's heights + 1.
// Modifies X16, X17, and X18
////////////////////////////////////////////////////////
.macro	calcNewHeight	reg
	ldr	X16, [\reg, #node_left]		// X16 = node->left
	cbz	X16, 1f				// if node->left is null, height is 0
	ldr	X16, [X16, #node_height]	// X16 = node->left->height
1:	ldr	X17, [\reg, #node_right]	// X17 = node->right
	cbz	X17, 2f				// if node->right is null, height is 0
	ldr	X17, [X17, #node_height]	// X17 = node->right->height
2:	cmp	X16, X17
	csel	X18, X16, X17, hi		// X18 = max(X16, X17)
	add	X18, X18, #1			// X18 = max(X16, X17) + 1
	str	X18, [\reg, #node_height]	// node->height = X18

////////////////////////////////////////////////////////
// Rotate the tree counter-clockwise at the given node.
////////////////////////////////////////////////////////
// Input:
//   X0 - Root
// Output:
//   X1 - New root
// Registers:
//   X0  - New root
//   X1  - Root
//   X16 - Left height
//   X17 - Right height
//   X18 - Scratch
rotateLeft:
	mov	X1, X0			// Copy root to X1
	// newRoot = root->right
	ldr	X0, [X1, #node_right]
	// root->right = newRoot->left
	ldr	X18, [X0, #node_left]
	str	X18, [X1, #node_right]
	// newRoot->left = root
	str	X1, [X0, #node_left]
	// root->height = max(root->left->height, root->right->height) + 1
	calcNewHeight	X0
	// newRoot->height = max(newRoot->left->height, newRoot->right->height) + 1
	calcNewHeight	X1
	ret

////////////////////////////////////////////////////////
// Rotate the tree clockwise at the given node.
////////////////////////////////////////////////////////
// Input:
//   X0 - Root
// Output:
//   X1 - New root
// Registers:
//   X0  - New root
//   X1  - Root
//   X16 - Left height
//   X17 - Right height
//   X18 - Scratch
rotateRight:
	mov	X1, X0			// Copy root to X1
	// newRoot = root->left
	ldr	X0, [X1, #node_left]
	// root->left = newRoot->right
	ldr	X18, [X0, #node_right]
	str	X18, [X1, #node_left]
	// newRoot->right = root
	str	X1, [X0, #node_right]
	// root->height = max(root->left->height, root->right->height) + 1
	calcNewHeight	X0
	// newRoot->height = max(newRoot->left->height, newRoot->right->height) + 1
	calcNewHeight	X1
	ret

////////////////////////////////////////////////////////
// Find the node for the given coordinate. Return null
// if the coordinate doesn't exist.
////////////////////////////////////////////////////////
// Input:
//   X0 - Root node
//   X1 - Coordinate value
// Output:
//   X0 - Node for this coordinate. NULL if not found.
// Registers:
//   X2 - Coordinate at this node.
//   X3 - Pointer to left child node.
//   X4 - Pointer to right child node.
findNode:
	cbz	X0, findDone		// If this node is NULL, the coordinate isn't in the list.
	ldr	X2, [X0, #node_coord]	// Load the coordinate value for this node.
	cmp	X1, X2			// Is this the coordinate we're looking for?
	b.eq	findDone			// Yes, return this node.
	ldr	X3, [X0, #node_left]	// Load pointer to left child.
	ldr	X4, [X0, #node_right]	// Load pointer to right child.
	// If the coordinate we're looking for is less than the one at this node, search
	// from the left child node, otherwise search from the right.
	csel	X0, X3, X4, lo
	b findNode
findDone:
	ret

////////////////////////////////////////////////////////
// Free all the nodes in the tree.
////////////////////////////////////////////////////////
// Input:
//   X0 - Root node
// Output:
//   None
// Registers:
//   X19 - Local copy of root node.
freeNodes:
	cbnz	X0, 1f
	ret
1:
	push2	LR, X19
	mov	X19, X0			// Save our local copy of root pointer.
	ldr	X0, [X19, #node_left]	// Free the left tree.
	bl freeNodes
	ldr	X0, [X19, #node_right]	// Free the right tree.
	bl freeNodes
	mov	X0, X19			// Copy pointer to root node to X0 for call to free.
	pop2	LR, X19			// Pop registers so free can return to our caller.
	b	free


////////////////////////////////////////////////////////
// Print the tree to a graphviz DOT file.
////////////////////////////////////////////////////////
// Input:
//   X0 - Root node
// Output:
//   None
// Registers:
//   X19 - Local copy of root node.
//   X20 - File handle of output file.
printTree:
	push2	LR, X19
	mov	X19, X0			// Save our local copy of root pointer.
	openFile	fileName, O_CREAT

	adds	X20, XZR, X0		// Save file handle and set flags.
	b.pl	outputOpenOk		// Positive value means file is open.
	mov	X1, #1			// stdout
	ldr	X2, =outputErrorLen	// Error message length.
	ldr	W2, [X2]
	writeFile	X1, outputError, X2	// Print the error message.
	b	printTreeDone

outputOpenOk:
	// Print the file prolog.
	mov	X0, X20			// File handle.
	ldr	X1, =fileProlog		// Pointer to file prolog string.
	bl	dprintf

	mov	X0, X19			// Pass root node as first argument to printNodes.
	mov	X1, X20			// Pass file handle as second argument to printNodes.
	bl	printNodes

	mov	X0, X20			// File handle.
	ldr	X2, =fileEpilog		// Pointer to file epilog string.
	bl	dprintf

	flushClose	X20

printTreeDone:
	pop2	LR, X19
	ret

outputError:
	.asciz	"Failed to open output file.\n"
outputErrorLen:
	.word	. - outputError
fileProlog:
	.asciz	"digraph nodes {\n    node [shape=plaintext]\n\n"