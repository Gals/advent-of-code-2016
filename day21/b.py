import sys
import re

class Operation(object):
	def __repr__(self):
		return '<%s>' % (
			self.__class__.__name__)

	def execute(self, data):
		raise NotImplementedError()

	def reverse(self, data):
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

	def reverse(self, data):
		reversed_operation = SwapPositionOperation(
			self.y,
			self.x)
		return reversed_operation.execute(data)

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

	def reverse(self, data):
		return self.execute(data)

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

	def reverse(self, data):
		reversed_operation = RotateRightOperation(self.steps)
		return reversed_operation.execute(data)

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

	def reverse(self, data):
		reversed_operation = RotateLeftOperation(self.steps)
		return reversed_operation.execute(data)

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

	def reverse(self, data): 
		steps = 1
		d = data
		# Try to restore the original string.
		# Rotate the string to the left, until the result 
		# of roating the string based on position, 
		# would give us the current string.
		while self.execute(d) != data:
			d = RotateLeftOperation(steps).execute(d)
			steps += 1
		return d

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

	def reverse(self, data):
		return self.execute(data)

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

	def reverse(self, data):
		reversed_operation = MovePositionOperation(
			self.y,
			self.x)
		return reversed_operation.execute(data)

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
	s = 'abcdefghij'
	assert SwapPositionOperation(0, 4).reverse(SwapPositionOperation(0, 4).execute(s)) == s
	assert RotateBasedOnPositionOperation('c').reverse(RotateBasedOnPositionOperation('c').execute(s)) == s

def reverse_operations(data, operation_lines, operation_set):
	for line in operation_lines:
		operation = None
		for operation_class in operation_set:
			operation = operation_class.parse(line)
			if operation:
				prev_data = data
				data = operation.reverse(data)
				break
		if operation is None:
			raise Exception('Failed to parse operation: %r' % (
				line))
	return data

def unscramble(data, operation_lines):
	return reverse_operations(
		data,
		operation_lines[::-1],
		OPERATIONS)

def main():
	test()
	data = sys.argv[1]
	operations_data = open(sys.argv[2], 'r').read()
	operation_lines = operations_data.split('\n')[:-1]

	print unscramble(data, operation_lines)

if __name__ == '__main__':
	main()