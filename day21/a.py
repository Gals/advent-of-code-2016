import sys
import re

class Operation(object):
	def __repr__(self):
		return '<%s>' % (
			self.__class__.__name__)

	def execute(self, data):
		raise NotImplementedError()

	@classmethod
	def parse(cls, line):
		raise NotImplementedError()

class SwapPositionOperation(Operation):
	OP_REGEX = re.compile('swap position (\d+) with position (\d+)')

	def __init__(self, x, y):
		self.x = x
		self.y = y

	def execute(self, data):
		tmp = data[self.x]
		result = list(data)
		result[self.x] = result[self.y]
		result[self.y] = tmp
		return ''.join(result)

	@classmethod
	def parse(cls, line):
		match = cls.OP_REGEX.match(line)
		if match is None:
			return

		x = int(match.group(1))
		y = int(match.group(2))
		return cls(x, y)

class SwapLetterOperation(Operation):
	OP_REGEX = re.compile('swap letter ([a-zA-Z]+) with letter ([a-zA-Z]+)')

	def __init__(self, x, y):
		self.x = x
		self.y = y

	def execute(self, data):
		result = data.replace(self.x, '$')
		result = result.replace(self.y, self.x)
		result = result.replace('$', self.y)
		return result

	@classmethod
	def parse(cls, line):
		match = cls.OP_REGEX.match(line)
		if match is None:
			return

		return cls(match.group(1), match.group(2))

class RotateLeftOperation(Operation):
	OP_REGEX = re.compile('rotate left (\d+) step(?:s?)')

	def __init__(self, steps):
		self.steps = steps

	def execute(self, data):
		steps = self.steps % len(data)
		if steps == 0:
			return data
		return data[steps:] + data[:steps]

	@classmethod
	def parse(cls, line):
		match = cls.OP_REGEX.match(line)
		if match is None:
			return

		steps = int(match.group(1))
		return cls(steps)

class RotateRightOperation(Operation):
	OP_REGEX = re.compile('rotate right (\d+) step(?:s?)')

	def __init__(self, steps):
		self.steps = steps

	def execute(self, data):
		steps = self.steps % len(data)
		if steps == 0:
			return data
		return data[-steps:] + data[:len(data) - steps]

	@classmethod
	def parse(cls, line):
		match = cls.OP_REGEX.match(line)
		if match is None:
			return

		steps = int(match.group(1))
		return cls(steps)

class RotateBasedOnPositionOperation(Operation):
	OP_REGEX = re.compile('rotate based on position of letter ([a-zA-Z])')

	def __init__(self, letter):
		self.letter = letter

	def execute(self, data):
		steps = 1
		index = data.find(self.letter)
		steps += index
		if index >= 4:
			steps += 1
		return RotateRightOperation(steps).execute(data)

	@classmethod
	def parse(cls, line):
		match = cls.OP_REGEX.match(line)
		if match is None:
			return

		return cls(match.group(1))

class ReversePositionsOperation(Operation):
	OP_REGEX = re.compile('reverse positions (\d+) through (\d+)')

	def __init__(self, x, y):
		self.x = x
		self.y = y

	def execute(self, data):
		start = self.x
		end = self.y + 1
		return data[:start] + data[start:end][::-1] + data[end:]

	@classmethod
	def parse(cls, line):
		match = cls.OP_REGEX.match(line)
		if match is None:
			return

		x = int(match.group(1))
		y = int(match.group(2))
		return cls(x, y)

class MovePositionOperation(Operation):
	OP_REGEX = re.compile('move position (\d+) to position (\d+)')

	def __init__(self, x, y):
		self.x = x
		self.y = y

	def execute(self, data):
		result = list(data)
		c = result.pop(self.x)
		result.insert(self.y, c)
		return ''.join(result)

	@classmethod
	def parse(cls, line):
		match = cls.OP_REGEX.match(line)
		if match is None:
			return

		x = int(match.group(1))
		y = int(match.group(2))
		return cls(x, y)

OPERATIONS = [
	SwapPositionOperation,
	SwapLetterOperation,
	RotateLeftOperation,
	RotateRightOperation,
	RotateBasedOnPositionOperation,
	ReversePositionsOperation,
	MovePositionOperation,
]

def test():
	s = 'abcde'
	s = SwapPositionOperation.parse('swap position 4 with position 0').execute(s)
	assert s == 'ebcda'
	s = SwapLetterOperation.parse('swap letter d with letter b').execute(s)
	assert s == 'edcba'
	s = ReversePositionsOperation.parse('reverse positions 0 through 4').execute(s)
	assert s == 'abcde'
	s = RotateLeftOperation.parse('rotate left 1 step').execute(s)
	assert s == 'bcdea'
	s = MovePositionOperation.parse('move position 1 to position 4').execute(s)
	assert s == 'bdeac'
	s = MovePositionOperation.parse('move position 3 to position 0').execute(s)
	assert s == 'abdec'
	s = RotateBasedOnPositionOperation.parse('rotate based on position of letter b').execute(s)
	assert s == 'ecabd'
	s = RotateBasedOnPositionOperation.parse('rotate based on position of letter d').execute(s)
	assert s == 'decab'

def execute_operations(data, operation_lines, operation_set):
	for line in operation_lines:
		operation = None
		for operation_class in operation_set:
			operation = operation_class.parse(line)
			if operation:
				data = operation.execute(data)
				break
		if operation is None:
			raise Exception('Failed to parse operation: %r' % (
				line))
	return data

def scramble(data, operation_lines):
	return execute_operations(
		data,
		operation_lines,
		OPERATIONS)

def main():
	# test()
	data = sys.argv[1]
	operations_data = open(sys.argv[2], 'r').read()
	operation_lines = operations_data.split('\n')[:-1]

	print scramble(data, operation_lines)

if __name__ == '__main__':
	main()