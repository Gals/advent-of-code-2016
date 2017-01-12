import sys
import re
from copy import deepcopy

class Node(object):
	def __init__(self, x, y, size=0, used=0, avail=0, use=0):
		self.x = x
		self.y = y
		self.size = size
		self.used = used
		self.avail = avail
		self.use = use

	def __repr__(self):
		return '<%s (%d, %d) %d/%d)>' % (
			self.__class__.__name__,
			self.x,
			self.y,
			self.used,
			self.size)

def parse_node_lines(lines):
	entry_regex = re.compile(
		'/dev/grid/node-x(?P<x>\d+)-y(?P<y>\d+)\s+(?P<size>\d+)T\s+(?P<used>\d+)T\s+(?P<avail>\d+)T\s+(?P<use>\d+)%')
	nodes = []

	for line in lines:
		match = entry_regex.match(line)
		if match is None:
			raise Exception('Failed to parse entry: %r' % (
				line))
		node = Node(
			x=int(match.group('x')),
			y=int(match.group('y')),
			size=int(match.group('size')),
			used=int(match.group('used')),
			avail=int(match.group('avail')),
			use=int(match.group('use'))
		)
		nodes.append(node)

	return nodes

def parse_df_output(output):
	lines = output.split('\n')[:-1]
	return parse_node_lines(lines[2:])

def find_goal(nodes):
	highest_x = 0
	goal = None
	for n in nodes:
		if n.y == 0 and n.x > highest_x:
			highest_x = n.x
			goal = n
	return goal

def find_empty_nodes(nodes):
	return [n for n in nodes if n.used == 0]

def build_grid(nodes):
	grid = []
	for n in nodes:
		x, y = n.x, n.y
		if len(grid) <= x:
			grid.insert(x, [])
		grid[x].insert(y, n)
	return grid

def get_state_hash(empty, goal):
	return str(empty) + str(goal)

def find_shortest_path_distance(goal, nodes):
	grid = build_grid(nodes)
	width = len(grid)
	height = len(grid[0])

	empty = find_empty_nodes(nodes)[0]
	queue = [(0, empty, goal)]
	seen = set()

	while len(queue) > 0:
		distance, empty, goal = queue.pop(0)

		for (dx, dy) in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
			x = empty.x + dx
			y = empty.y + dy
			if (x < 0 or y < 0) or \
				(x + 1 > width or y + 1 > height):
				# Invalid coordinates.
				continue
			
			neighbour = grid[x][y]
			if neighbour.used > empty.size:
				continue

			if neighbour.x == goal.x and neighbour.y == goal.y:
				state_hash = get_state_hash(neighbour, empty)
				if state_hash in seen:
					continue

				queue.append((distance + 1, neighbour, empty))
				seen.add(state_hash)
				continue

			if goal.x == 0 and goal.y == 0:
				return distance

			state_hash = get_state_hash(neighbour, goal)
			if state_hash in seen:
				continue

			queue.append((distance + 1, neighbour, goal))
			seen.add(state_hash)

def main():
	data = open(sys.argv[1], 'r').read()
	nodes = parse_df_output(data)
	goal = find_goal(nodes)
	print find_shortest_path_distance(goal, nodes)

if __name__ == '__main__':
	main()