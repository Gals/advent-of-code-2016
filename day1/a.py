import sys

def parse_instructions_file(file_path):
	instructions = []
	instructions_data = open(file_path, 'rb').read().strip()
	for instruction in instructions_data.split(', '):
		direction = instruction[:1]
		blocks = int(instruction[1:])
		instructions.append((direction, blocks))
	return instructions

def calculate_dest_point(instructions):
	x = 0
	y = 0
	axis = 'x'
	dir_factor = 1
	for direction, blocks in instructions:
		if direction == 'R':
			if axis == 'x':
				x += blocks * dir_factor
			elif axis == 'y':
				dir_factor *= -1
				y += blocks * dir_factor
		elif direction == 'L':
			if axis == 'x':
				dir_factor *= -1
				x += blocks * dir_factor
			elif axis == 'y':
				y += blocks * dir_factor
		if axis == 'x':
			axis = 'y'
		elif axis == 'y':
			axis = 'x'

	return (x, y)

def main():
	# instructions = [('R', 2), ('R', 2), ('R', 2)]
	# instructions = [('R', 2), ('L', 3)]
	# instructions = [('R', 5), ('L', 5), ('R', 5), ('R', 3)]
	instructions = parse_instructions_file(sys.argv[1])
	(x, y) = calculate_dest_point(instructions)
	print x, y
	print abs(x) + abs(y)

if __name__ == '__main__':
	main()