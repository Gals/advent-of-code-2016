import sys
import re

def parse_triangles_file(file_path):
	triangles = []
	with open(file_path, 'r') as sides_file:
		temp_triangles = [[], [], []]
		sides_count = 0
		for line in sides_file:
			sides = map(int, re.findall('\d+', line))
			for i, side in enumerate(sides):
				temp_triangles[i].append(side)
			sides_count += 1
			if sides_count == 3:
				triangles.extend(temp_triangles)
				temp_triangles = [[], [], []]
				sides_count = 0

	return triangles

def is_valid_triangle(sides):
	if sides[0] + sides[1] <= sides[2]:
		return False

	if sides[0] + sides[2] <= sides[1]:
		return False

	if sides[2] + sides[1] <= sides[0]:
		return False

	return True

def main():
	triangles = parse_triangles_file(sys.argv[1])
	print triangles
	valid_triangles = filter(is_valid_triangle, triangles)
	print 'Valid triangles: %d (out of %d)' % (
		len(valid_triangles),
		len(triangles))

if __name__ == '__main__':
	main()