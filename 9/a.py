import sys
import re

def decompress(data):
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
				
				sequence = data[i + 1:i + 1 + length]
				# Ignore whitespace.
				sequence =  re.sub('\s+', '', sequence)

				decompressed += sequence * times
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
		decompressed += c
		i += 1

	return decompressed

def main():
	# decompress_tests = [
	# 	('ADVENT', 'ADVENT'),
	# 	('A(1x5)BC', 'ABBBBBC'),
	# 	('(3x3)XYZ', 'XYZXYZXYZ'),
	# 	('A(2x2)BCD(2x2)EFG', 'ABCBCDEFEFG'),
	# 	('(6x1)(1x3)A', '(1x3)A'),
	# 	('X(8x2)(3x3)ABCY', 'X(3x3)ABC(3x3)ABCY')
	# ]
	# for data, decompressed in decompress_tests:
	# 	assert decompress(data) == decompressed

	data = open(sys.argv[1], 'rb').read()
	decompressed = decompress(data)
	print 'Decompressed length: %d' % (len(decompressed))

if __name__ == '__main__':
	main()