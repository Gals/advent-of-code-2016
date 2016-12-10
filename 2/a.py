import sys

KEYPAD_DIRECTIONS_MAP = {
	1: {'U': None, 'D': 4, 'R': 2, 'L': None},
	2: {'U': None, 'D': 5, 'R': 3, 'L': 1},
	3: {'U': None, 'D': 6, 'R': None, 'L': 2},

	4: {'U': 1, 'D': 7, 'R': 5, 'L': None},
	5: {'U': 2, 'D': 8, 'R': 6, 'L': 4},
	6: {'U': 3, 'D': 9, 'R': None, 'L': 5},

	7: {'U': 4, 'D': None, 'R': 8, 'L': None},
	8: {'U': 5, 'D': None, 'R': 9, 'L': 7},
	9: {'U': 6, 'D': None, 'R': None, 'L': 8},
}

def parse_instructions_file(file_path):
	instructions = []
	instructions_data = open(file_path, 'rb').read().strip()
	for directions in instructions_data.split('\n'):
		instructions.append(list(directions))
	return instructions

def main():
	instructions = parse_instructions_file(sys.argv[1])
	# instructions = [
	# 	list('ULL'),
	# 	list('RRDDD'),
	# 	list('LURDL'),
	# 	list('UUUUD')
	# ]
	keys = []
	current_key = 5
	for directions in instructions:
		for direction in directions:
			print current_key, direction
			new_key = KEYPAD_DIRECTIONS_MAP[current_key][direction]
			if not new_key:
				# Skip this instruction, as it does not
				# lead to a new key.
				continue
			else:
				current_key = new_key
		keys.append(current_key)
	print keys
	print ''.join(map(str, keys))

if __name__ == '__main__':
	main()