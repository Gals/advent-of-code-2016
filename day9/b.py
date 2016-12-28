import sys
import re
import os

def calculate_decompressed_length(data, decompressed_length=0):
	decompressed = ''
	parenthesis_open = False
	parenthesis_data = ''
	i = 0
	while i < len(data):
		c = data[i]

		# Ignore whitespace.
		if re.match('\s', c):
			i += 1
			continue

		if c == '(' and not parenthesis_open:
			parenthesis_open = True
			i += 1
			continue

		if c == ')' and parenthesis_open:
			marker_match = re.match('(\d+)x(\d+)', parenthesis_data)
			if marker_match:
				length = int(marker_match.group(1))
				times = int(marker_match.group(2))
				# Decompress markers inside this sequence.
				decompressed_sequence_length = calculate_decompressed_length(
					data[i + 1:i + 1 + length])
				decompressed_length += decompressed_sequence_length * times
				i += length + 1
			else:
				i += 1

			parenthesis_open  = False
			parenthesis_data = ''
			continue

		if parenthesis_open:
			parenthesis_data += c
			i += 1
			continue

		# No changes.
		decompressed_length += 1
		i += 1

	return decompressed_length

def main():
# 	decompress_tests = [
# 		('(3x3)XYZ', len('XYZXYZXYZ')),
# 		('X(8x2)(3x3)ABCY', len('XABCABCABCABCABCABCY')),
# 		('(27x12)(20x12)(13x14)(7x10)(1x12)A', 241920),
# 		('(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN', 445),
# 	]
# 	for data, decompressed_length in decompress_tests:
# 		assert calculate_decompressed_length(data) == decompressed_length
	
	data = open(sys.argv[1], 'rb').read()
	decompressed_length = calculate_decompressed_length(data)
	print 'Decompressed length: %d' % (decompressed_length)

if __name__ == '__main__':
	main()