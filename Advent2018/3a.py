import re

repattern = re.compile(r"#(\d*) @ (\d*),(\d*): (\d*)x(\d*)")
fabric = {}
overlapping_claims = set()
all_claims = set()
with open("3.txt", "r") as infile:
	for line in infile:
		print(line.strip())
		result = repattern.match(line.strip())
		claim_number, left_offset, top_offset, width, height = \
			int(result[1]), int(result[2]), int(result[3]), int(result[4]), int(result[5])
		all_claims.add(claim_number)
		#print(claim_number, left_offset, right_offset, width, height)
		for x in range(left_offset, left_offset + width):
			for y in range(top_offset, top_offset + height):
				coordinate = (x, y)
				#print(coordinate)
				if not coordinate in fabric:
					fabric[coordinate] = [claim_number]
				else:
					fabric[coordinate].append(claim_number)
					
overlaps = 0
for fabric_square in fabric.values():
	if len(fabric_square) > 1:
		overlapping_claims.update(fabric_square)
		overlaps += 1
print(overlaps)
print(all_claims - overlapping_claims)
