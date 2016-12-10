import sys

KEYPAD_DIRECTIONS_MAP = {
	'1': {'U': None, 'D': '3', 'R': None, 'L': None},

	'2': {'U': None, 'D': '6', 'R': '3', 'L': None},
	'3': {'U': '1', 'D': '7', 'R': '4', 'L': '2'},
	'4': {'U': None, 'D': '8', 'R': None, 'L': '3'},

	'5': {'U': None, 'D': None, 'R': '6', 'L': None},
	'6': {'U': '2', 'D': 'A', 'R': '7', 'L': '5'},
	'7': {'U': '3', 'D': 'B', 'R': '8', 'L': '6'},
	'8': {'U': '4', 'D': 'C', 'R': '9', 'L': '7'},
	'9': {'U': None, 'D': None, 'R': None, 'L': '8'},

	'A': {'U': '6', 'D': None, 'R': 'B', 'L': None},
	'B': {'U': '7', 'D': 'D', 'R': 'C', 'L': 'A'},
	'C': {'U': '8', 'D': None, 'R': None, 'L': 'B'},

	'D': {'U': 'B', 'D': None, 'R': None, 'L': None},
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
	current_key = '5'
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