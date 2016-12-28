import sys
import re

class Register(object):
	def __init__(self, name, value=0):
		self.name = name
		self.value = value

	def __repr__(self):
		return '<%s [%r: %d]>' % (
			self.__class__.__name__,
			self.name,
			self.value)

class ExecutionContext(object):
	def __init__(self, registers=None, stack=None, ip=0):
		self.registers = registers or {}
		self.stack = stack or []
		self.instruction_pointer = ip

	def execute(self):
		while self.instruction_pointer < len(self.stack):
			next_instruction = self.stack[self.instruction_pointer]
			next_instruction.execute(self)
			self.instruction_pointer += 1
			print self

	def __repr__(self):
		return '<%s [IP: %d, %r]>' % (
			self.__class__.__name__,
			self.instruction_pointer,
			self.registers)

	def print_stack(self):
		pass

class Instruction(object):
	"""Represents Assembunny instruction."""
	def __repr__(self):
		return '<%s>' % (
			self.__class__.__name__)

	def execute(self, context):
		raise NotImplementedError()

	@classmethod
	def parse(cls, line):
		raise NotImplementedError()

class UnaryInstruction(Instruction):
	def __init__(self, a):
		super(UnaryInstruction, self).__init__()
		self.a = a

class BinaryInstruction(Instruction):
	def __init__(self, a, b):
		super(BinaryInstruction, self).__init__()
		self.a = a
		self.b = b

	def get_first_operand_value(self, context):
		if isinstance(self.a, str):
			return context.registers[self.a].value
		elif isinstance(self.a, int):
			return self.a
		else:
			raise ValueError('First operand should be a string or an integer.')

class CpyInstruction(BinaryInstruction):
	INSTRUCTION_REGEX = re.compile('cpy ([\da-z]+) ([\da-z]+)')

	def execute(self, context):
		value = self.get_first_operand_value(context)
		context.registers[self.b].value = value

	@classmethod
	def parse(cls, line):
		match = cls.INSTRUCTION_REGEX.match(line)
		if match is None:
			return

		a = match.group(1)
		try:
			a = int(a)
		except ValueError:
			pass
		b = match.group(2)
		return cls(a, b)

class IncInstruction(UnaryInstruction):
	INSTRUCTION_REGEX = re.compile('inc ([\da-z]+)')

	def execute(self, context):
		context.registers[self.a].value += 1

	@classmethod
	def parse(cls, line):
		match = cls.INSTRUCTION_REGEX.match(line)
		if match is None:
			return

		a = match.group(1)
		return cls(a)

class DecInstruction(UnaryInstruction):
	INSTRUCTION_REGEX = re.compile('dec ([\da-z]+)')

	def execute(self, context):
		context.registers[self.a].value -= 1

	@classmethod
	def parse(cls, line):
		match = cls.INSTRUCTION_REGEX.match(line)
		if match is None:
			return

		a = match.group(1)
		return cls(a)

class JnzInstruction(BinaryInstruction):
	INSTRUCTION_REGEX = re.compile('jnz ([\-\da-z]+) ([\-\d]+)')

	def execute(self, context):
		value = self.get_first_operand_value(context)
		if value == 0:
			return
		context.instruction_pointer += (self.b - 1)

	@classmethod
	def parse(cls, line):
		match = cls.INSTRUCTION_REGEX.match(line)
		if match is None:
			return

		a = match.group(1)
		try:
			a = int(a)
		except ValueError:
			pass
		b = int(match.group(2))
		return cls(a, b)

INSTRUCTION_SET = [
	CpyInstruction,
	IncInstruction,
	DecInstruction,
	JnzInstruction,
]

def resolve_name_conflict(name, names):
	new_name = name
	tries = 0
	while new_name in names:
		tries += 1
		new_name = '%s%d' % (name, tries)
	return new_name

def parse_instruction_lines(lines, instruction_set):
	instructions = []
	for line in lines:
		instruction = None
		for instruction_class in instruction_set:
			instruction = instruction_class.parse(line)
			if instruction is not None:
				instructions.append(instruction)
				break
		if instruction is None:
			raise Exception('Unsupported instruction line: %r' % (
				line))
	return instructions

def execution_context_factory(registers_number, stack=None):
	stack = stack or []

	registers = {}
	names = []
	for i in xrange(registers_number):
		name = chr(ord('a') + (i % (ord('z') - ord('a') + 1)))
		if name in names:
			name = resolve_name_conflict(name, names)
		names.append(name)
		registers[name] = Register(name)

	return ExecutionContext(
		registers=registers,
		stack=stack)

def test():
	instruction_lines = [
		'cpy 41 a',
		'inc a',
		'inc a',
		'dec a',
		'jnz a 2',
		'dec a'
	]
	stack = parse_instruction_lines(
		instruction_lines,
		INSTRUCTION_SET)
	context = execution_context_factory(
		registers_number=4,
		stack=stack)
	
	print context
	context.execute()
	print context.registers['a']
	assert context.registers['a'].value, 42

def part_a(instruction_lines):
	stack = parse_instruction_lines(
		instruction_lines,
		INSTRUCTION_SET)
	context = execution_context_factory(
		registers_number=4,
		stack=stack)

	print context
	context.execute()
	print context.registers['a']

def part_b(instruction_lines):
	stack = parse_instruction_lines(
		instruction_lines,
		INSTRUCTION_SET)
	context = execution_context_factory(
		registers_number=4,
		stack=stack)
	context.registers['c'].value = 1

	print context
	context.execute()
	print context.registers['a']

def main():
	test()

	instruction_lines = open(sys.argv[1], 'r').read().split('\n')[:-1]
	# part_a(instruction_lines)
	part_b(instruction_lines)

if __name__ == '__main__':
	main()