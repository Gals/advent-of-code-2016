import sys
import re

class Disc(object):
	DISC_REGEX = re.compile(
		'Disc #([\d]+) has ([\d]+) positions; at time=0, it is at position ([\d]+).')

	def __init__(self, index, positions, start_position=0):
		self.index = index
		self.positions = positions
		self.start_position = start_position

	def __repr__(self):
		return '<%s [#%d: %d (%d positions)]>' % (
			self.__class__.__name__,
			self.index,
			self.start_position,
			self.positions)

	@classmethod
	def parse(cls, line):
		match = cls.DISC_REGEX.match(line)
		if match is None:
			raise Exception('Failed to parse disc line: %r' % (
				line))

		return cls(
			index=int(match.group(1)),
			positions=int(match.group(2)),
			start_position=int(match.group(3))
		)

def disc_position_at_tick(disc, tick):
	ticks = disc.index + tick
	return (disc.start_position + ticks) % disc.positions

def parse_discs_lines(lines):
	discs = []
	for line in lines:
		discs.append(Disc.parse(line))
	return discs

def ticks_to_get_capsule(discs):
	ticks = 0
	while True:
		positions = [disc_position_at_tick(d, ticks) for d in discs]
		if sum(positions) == 0:
			break
		ticks += 1
	return ticks

def test():
	discs = [Disc(1, 4, 5), Disc(2, 1, 2)]
	assert ticks_to_get_capsule(discs) == 5

def main():
	# test()
	data = open(sys.argv[1], 'r').read()
	lines = data.split('\n')[:-1]
	discs = parse_discs_lines(lines)
	print ticks_to_get_capsule(discs)

if __name__ == '__main__':
	main()