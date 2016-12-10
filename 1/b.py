import sys

class Point(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __repr__(self):
		return '<%s (%d, %d)>' % (
			self.__class__.__name__,
			self.x,
			self.y)

def parse_instructions_file(file_path):
	instructions = []
	instructions_data = open(file_path, 'rb').read().strip()
	for instruction in instructions_data.split(', '):
		direction = instruction[:1]
		blocks = int(instruction[1:])
		instructions.append((direction, blocks))
	return instructions

def visit_points(instructions, visit_callback, *args):
	"""Fires the callback for each point visited,
	according to the instructions."""
	x = 0
	y = 0
	p = Point(0, 0)
	visit_callback(p, 1, 0, *args)

	axis = 'x'
	m = 1
	for direction, blocks in instructions:
		previous_point = p

		if direction == 'R':
			if axis == 'x':
				x += blocks * m
			elif axis == 'y':
				m *= -1
				y += blocks * m
		elif direction == 'L':
			if axis == 'x':
				m *= -1
				x += blocks * m
			elif axis == 'y':
				y += blocks * m

		p = Point(x, y)
		if not visit_callback(p, m, blocks, *args):
			break

		if axis == 'x':
			axis = 'y'
		elif axis == 'y':
			axis = 'x'

def point_visited(p, visited):
	"""Checks to see if point `p` has been visited."""
	for i, current_point in enumerate(visited[1:], 1):
		previous_point = visited[i - 1]
		if current_point.x == p.x:
			if p.y >= previous_point.y and p.y <= current_point.y:
				return True
		elif current_point.y == p.y:
			if p.x >= previous_point.x and p.x <= current_point.x:
				return True
	return False

def stop_when_visited_twice_callback(p, m, blocks, visited, 
	visited_twice_callback):
	print p

	# We need at least a couple of points.
	if len(visited) < 1:
		visited.append(p)
		return True

	previous_point = visited[-1]
	delta_x = abs(p.x - previous_point.x)
	delta_y = abs(p.y - previous_point.y)

	if delta_x > 0:
		for i in xrange(1, blocks + 1):
			# Test the points we've visited on X axis.
			test_point = Point(previous_point.x + i * m, p.y)
			if point_visited(test_point, visited):
				visited_twice_callback(test_point)
				return False
	elif delta_y > 0:
		for i in xrange(1, blocks + 1):
			# Test the points we've visited on Y axis.
			test_point = Point(p.x, previous_point.y + i * m)
			if point_visited(test_point, visited):
				visited_twice_callback(test_point)
				return False

	visited.append(p)
	return True

def visited_twice_callback(p):
	print 'Visited twice ---> %s' % (p)
	print abs(p.x) + abs(p.y)

def main():
	instructions = parse_instructions_file(sys.argv[1])
	# instructions = [('R', 8), ('R', 4), ('R', 4), ('R', 8)]
	visited = []
	visit_points(
		instructions,
		stop_when_visited_twice_callback,
		visited,
		visited_twice_callback)

if __name__ == '__main__':
	main()