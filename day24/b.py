import sys
import itertools

def parse_grid(rows):
	nodes = {}
	for row, columns in enumerate(rows[1:-1]):
		for column, data in enumerate(columns[1:-1]):
			try:
				node_id = int(data)
			except ValueError:
				continue
			x = column + 1
			y = row + 1
			nodes[node_id] = (x, y)
	return nodes

def find_shortest_path_bfs(src, dst, rows):
	dst_x, dst_y = dst

	w = len(rows[0])
	h = len(rows)

	queue = [([], src)]
	visited = []

	while len(queue) > 0:
		path, (x, y) = queue.pop(0)

		if x == dst_x and y == dst_y:
			return path 

		for (dx, dy) in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
			neighbour_x = x + dx
			neighbour_y = y + dy
			if neighbour_x < 1 or neighbour_y < 1 or \
				neighbour_x + 1 > w or neighbour_y + 1 > h:
				# Invalid coordinates.
				continue
			if rows[neighbour_y][neighbour_x] == '#':
				# Hits a wall.
				continue

			neighbour = (neighbour_x, neighbour_y)
			if neighbour in visited:
				continue

			queue.append((path + [neighbour], neighbour))
			visited.append(neighbour)

	raise Exception(
		'Failed to find a path from %r to %r' % (src, dst))

def pairwise(iterable):
    a, b = itertools.tee(iterable)
    next(b, None)
    return itertools.izip(a, b)

def solve(nodes, rows):
	shortest_distance = float('inf')
	distances = {}

	# We need to visit node '0' twice.
	nodes_to_visit = nodes.keys() + [0]

	for candidate_path in itertools.permutations(nodes_to_visit):
		# Filter out paths which don't start at node '0'
		# or don't end at '0'.
		if candidate_path[0] != 0 or candidate_path[-1] != 0:
			continue

		total_distance = 0
		for a, b in pairwise(candidate_path):
			distance = distances.get((a, b))
			if distance is None:
				shortest_path = find_shortest_path_bfs(
					nodes[a],
					nodes[b],
					rows)
				distance = len(shortest_path)
				# Cache distances from 'a' to 'b'.
				# Distance from 'b' to 'a' is equivalent, cache it too.
				distances[(a, b)] = distance
				distances[(b, a)] = distance
			total_distance += distance
		shortest_distance = min(shortest_distance, total_distance)

	return shortest_distance

def main():
	data = open(sys.argv[1], 'r').read()
	rows = data.split('\n')[:-1]
	nodes = parse_grid(rows)

	print solve(nodes, rows)

if __name__ == '__main__':
	main()