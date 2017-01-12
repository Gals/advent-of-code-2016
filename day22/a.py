import sys
import re

class Node(object):
	def __init__(self, x, y, size=0, used=0, avail=0, use=0):
		self.x = x
		self.y = y
		self.size = size
		self.used = used
		self.avail = avail
		self.use = use

	def __repr__(self):
		return '<%s (%d, %d)>' % (
			self.__class__.__name__,
			self.x,
			self.y)

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
			use=int(match.group('avail'))
		)
		nodes.append(node)

	return nodes

def parse_df_output(output):
	lines = output.split('\n')[:-1]
	return parse_node_lines(lines[2:])

def is_viable_pair(a, b):
	if a.used == 0:
		# Empty node.
		return False

	if a.x == b.x and a.y == b.y:
		# This is the same node.
		return False

	return b.avail >= a.used

def viable_pairs(nodes):
	viable_pairs = []

	for a in nodes:
		if a.used == 0:
			# Empty node.
			continue
		for b in nodes:
			if is_viable_pair(a, b):
				viable_pairs.append((a, b))

	return viable_pairs


def main():
	data = open(sys.argv[1], 'r').read()
	nodes = parse_df_output(data)
	print len(viable_pairs(nodes))

if __name__ == '__main__':
	main()