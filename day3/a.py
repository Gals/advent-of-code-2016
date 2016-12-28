import sys
import re

def parse_triangles_file(file_path):
	triangles = []
	with open(file_path, 'r') as sides_file:
		for line in sides_file:
			sides = map(int, re.findall('\d+', line))
			triangles.append(sides)
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
	valid_triangles = filter(is_valid_triangle, triangles)
	print 'Valid triangles: %d (out of %d)' % (
		len(valid_triangles),
		len(triangles))

if __name__ == '__main__':
	main()