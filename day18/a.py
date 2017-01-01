import sys

SAFE_TILE = '.'
TRAPPED_TILE = '^'

def get_from_list(l, i, default=None):
	if i < 0 or i >= len(l):
		return default
	return l[i]

def get_tile_at(row, column, rows):
	previous_row = rows[row - 1]
	left = get_from_list(previous_row, column - 1) == TRAPPED_TILE
	center = previous_row[column] == TRAPPED_TILE
	right = get_from_list(previous_row, column + 1) == TRAPPED_TILE

	trap_scenarios = (
		(True, True, False),
		(False, True, True),
		(True, False, False),
		(False, False, True)
	)
	
	if (left, center, right) in trap_scenarios:
		return TRAPPED_TILE
	
	return SAFE_TILE

def build_rows(first_row, rows_number):
	rows = [first_row]
	for row in xrange(rows_number - 1):
		columns = rows[row]
		new_column = ''
		for col, _ in enumerate(columns):
			new_column += get_tile_at(row + 1, col, rows)
		rows.append(new_column)
	return rows

def count_safe_tiles(rows):
	return sum([r.count(SAFE_TILE) for r in rows])

def test():
	rows = [
		'..^^.',
		'.^^^^',
		'^^..^'
	]
	assert build_rows(rows[0], len(rows)) == rows

	rows = [
		'.^^.^.^^^^',
		'^^^...^..^',
		'^.^^.^.^^.',
		'..^^...^^^',
		'.^^^^.^^.^',
		'^^..^.^^..',
		'^^^^..^^^.',
		'^..^^^^.^^',
		'.^^^..^.^^',
		'^^.^^^..^^'
	]
	assert build_rows(rows[0], len(rows)) == rows
	assert count_safe_tiles(rows) == 38

def main():
	# test()
	first_row = open(sys.argv[1], 'r').read().strip()
	# rows = build_rows(first_row, 40)
	rows = build_rows(first_row, 400000)
	print count_safe_tiles(rows)

if __name__ == '__main__':
	main()