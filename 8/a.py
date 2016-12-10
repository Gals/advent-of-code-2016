import sys
import re

class PixelState:
	ON = 1
	OFF = 0

class Instruction(object):
	def execute(self, screen):
		raise NotImplementedError()

class RectInstruction(object):
	INSTRUCTION_REGEX = re.compile('rect (\d+)x(\d+)')

	def __init__(self, width, height):
		self.width = width
		self.height = height

	def execute(self, screen):
		for x in xrange(self.width):
			for y in xrange(self.height):
				screen.pixels[y][x] = PixelState.ON

	def __repr__(self):
		return '<%s [%dx%d]>' % (
			self.__class__.__name__,
			self.width,
			self.height)

	@classmethod
	def parse(cls, line):
		match = cls.INSTRUCTION_REGEX.match(line)
		if not match:
			return

		width = int(match.group(1))
		height = int(match.group(2))
		return cls(width, height)

class RotateColumnInstruction(object):
	INSTRUCTION_REGEX = re.compile('rotate column x=(\d+) by (\d+)')

	def __init__(self, column, by):
		self.column = column
		self.by = by

	def execute(self, screen):
		# Keep track of the current column for reference.
		current_column = screen.column(self.column)

		for y, pixel in enumerate(current_column):
			new_y = (y + self.by) % screen.height
			screen.pixels[new_y][self.column] = pixel

	def __repr__(self):
		return '<%s [column %d by %d]>' % (
			self.__class__.__name__,
			self.column,
			self.by)

	@classmethod
	def parse(cls, line):
		match = cls.INSTRUCTION_REGEX.match(line)
		if not match:
			return

		column = int(match.group(1))
		by = int(match.group(2))
		return cls(column, by)

class RotateRowInstruction(object):
	INSTRUCTION_REGEX = re.compile('rotate row y=(\d+) by (\d+)')

	def __init__(self, row, by):
		self.row = row
		self.by = by

	def execute(self, screen):
		# Keep track of the current column for reference.
		current_row = screen.row(self.row)

		for x, pixel in enumerate(current_row):
			new_x = (x + self.by) % screen.width
			screen.pixels[self.row][new_x] = pixel

	def __repr__(self):
		return '<%s [row %d by %d]>' % (
			self.__class__.__name__,
			self.row,
			self.by)

	@classmethod
	def parse(cls, line):
		match = cls.INSTRUCTION_REGEX.match(line)
		if not match:
			return

		row = int(match.group(1))
		by = int(match.group(2))
		return cls(row, by)

class Screen(object):
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.pixels = []
		self._create_pixels()

	def _create_pixels(self):
		for x in xrange(self.height):
			row_pixels = []
			for y in xrange(self.width):
				row_pixels.append(PixelState.OFF)
			self.pixels.append(row_pixels)

	def column(self, column):
		"""Returns a copy of the specified column.
		"""
		pixels = []
		for y in xrange(self.height):
			pixels.append(self.pixels[y][column])
		return pixels

	def row(self, row):
		"""Returns a copy of the specified row.
		"""
		return self.pixels[row][:]

	def __repr__(self):
		return '<%s [%dx%d]>' % (
			self.__class__.__name__,
			self.width,
			self.height)

def print_screen(s):
	for row in s.pixels:
		for pixel in row:
			char = '#' if pixel == 1 else '.'
			print char,
		print
	print

INSTRUCTION_SET = [
	RectInstruction,
	RotateColumnInstruction,
	RotateRowInstruction,
]

def execute_instruction(instruction_set, line, screen):
	for instruction_class in instruction_set:
		instruction = instruction_class.parse(line)
		if not instruction:
			continue
		instruction.execute(screen)

def main():
	# screen = Screen(7, 3)
	# instructions = [
	# 	'rect 3x2',
	# 	'rotate column x=1 by 1',
	# 	'rotate row y=0 by 4',
	# 	'rotate column x=1 by 1'
	# ]

	screen = Screen(50, 6)
	instructions = open(sys.argv[1], 'r').read().split('\n')[:-1]

	for instruction in instructions:
		execute_instruction(
			INSTRUCTION_SET,
			instruction,
			screen)
	print_screen(screen)

	# Count lit pixels
	lit_pixels = sum([sum(row) for row in screen.pixels])
	print 'Lit pixels: %d (out of %d)' % (
		lit_pixels,
		screen.width * screen.height)


if __name__ == '__main__':
	main()