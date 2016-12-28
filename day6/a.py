import sys

def list_most_frequent_letters(rows):
	"""Returns a list of the most frequent letter
	in each column."""
	width = len(rows[0])
	letters_count = [{} for _ in xrange(width)]

	# Count the instances of each letter in a column.
	for row in rows:
		for col, letter in enumerate(list(row)):
			if not letters_count[col].has_key(letter):
				letters_count[col][letter] = 0
			letters_count[col][letter] += 1

	# Find the most frequent letters in each column.
	frequent_letters = []
	for column_letters_count in letters_count:
		frequent_letter = sorted(
			column_letters_count,
			key=column_letters_count.__getitem__,
			reverse=True)[0]
		frequent_letters.append(frequent_letter)
	return frequent_letters

def main():
	lines = open(sys.argv[1], 'rb').readlines()
	print ''.join(list_most_frequent_letters(lines))

if __name__ == '__main__':
	main()