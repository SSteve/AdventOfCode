import pdb

class Node:
	def __init__(self):
		self.childCount = 0
		self.metadataCount = 0
		self.children = []
		self.metadata = []
		
	def read(self, license):
		self.childCount = int(license.pop(0))
		self.metadataCount = int(license.pop(0))
		for i in range(self.childCount):
			self.children.append(Node())
			self.children[i].read(license)
		for i in range(self.metadataCount):
			self.metadata.append(int(license.pop(0)))
			
	def metadataSum(self):
		total = sum(self.metadata)
		for child in self.children:
			total += child.metadataSum()
		return total
		
	def nodeValue(self):
		if self.childCount == 0:
			return sum(self.metadata)
		else:
			total = 0
			for metaValue in self.metadata:
				if metaValue > 0 and metaValue <= self.childCount:
					total += self.children[metaValue-1].nodeValue()
			return total

with open("8.txt", "r") as infile:
	for line in infile:
		license = line.strip().split(' ')
		
tree = Node()
#pdb.set_trace()
tree.read(license)
print(tree.nodeValue())
