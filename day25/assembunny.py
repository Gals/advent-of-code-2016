import re

class InvalidInstructionError(Exception):
	pass

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

class ClockSignalExecutionContext(ExecutionContext):
	def __init__(self, registers=None, stack=None, ip=0):
		super(ClockSignalExecutionContext, self).__init__(
			registers,
			stack,
			ip)
		self.clock_signal = []

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

	def get_operand_value(self, context):
		if isinstance(self.a, str):
			return context.registers[self.a].value
		elif isinstance(self.a, int):
			return self.a
		else:
			raise ValueError('Operand should be a string or an integer.')

	def __repr__(self):
		return '<%s [%r]>' % (
			self.__class__.__name__,
			self.a)

class BinaryInstruction(Instruction):
	def __init__(self, a, b):
		super(BinaryInstruction, self).__init__()
		self.a = a
		self.b = b

	def __repr__(self):
		return '<%s [%r %r]>' % (
			self.__class__.__name__,
			self.a,
			self.b)

	def get_first_operand_value(self, context):
		if isinstance(self.a, str):
			return context.registers[self.a].value
		elif isinstance(self.a, int):
			return self.a
		else:
			raise ValueError('First operand should be a string or an integer.')

	def get_second_operand_value(self, context):
		if isinstance(self.b, str):
			return context.registers[self.b].value
		elif isinstance(self.b, int):
			return self.b
		else:
			raise ValueError('Second operand should be a string or an integer.')

class CpyInstruction(BinaryInstruction):
	INSTRUCTION_REGEX = re.compile('cpy ([\-\da-z]+) ([a-z]+)')

	def execute(self, context):
		if not isinstance(self.b, str):
			raise InvalidInstructionError('Second operand should be a string.')

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
	INSTRUCTION_REGEX = re.compile('jnz ([\-\da-z]+) ([\-\da-z]+)')

	def execute(self, context):
		value = self.get_first_operand_value(context)
		if value == 0:
			return
		
		offset = self.get_second_operand_value(context)
		context.instruction_pointer += (offset - 1)

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
		try:
			b = int(b)
		except ValueError:
			pass
		return cls(a, b)

class TglInstruction(UnaryInstruction):
	INSTRUCTION_REGEX = re.compile('tgl ([\-\da-z]+)')

	def get_operand_value(self, context):
		if isinstance(self.a, str):
			return context.registers[self.a].value
		elif isinstance(self.a, int):
			return self.a
		else:
			raise ValueError('First operand should be a string or an integer.')

	def execute(self, context):
		offset = self.get_operand_value(context)
		toggled_index = context.instruction_pointer + offset
		if toggled_index < 0 or toggled_index >= len(context.stack):
			# Outside of the program.
			return

		toggled = context.stack[toggled_index]

		if isinstance(toggled, IncInstruction):
			new_instruction = DecInstruction(toggled.a)
		elif isinstance(toggled, DecInstruction):
			new_instruction = IncInstruction(toggled.a)
		elif isinstance(toggled, UnaryInstruction):
			new_instruction = IncInstruction(toggled.a)
		elif isinstance(toggled, JnzInstruction):
			new_instruction = CpyInstruction(toggled.a, toggled.b)
		elif isinstance(toggled, BinaryInstruction):
			new_instruction = JnzInstruction(toggled.a, toggled.b)

		context.stack[toggled_index] = new_instruction

	@classmethod
	def parse(cls, line):
		match = cls.INSTRUCTION_REGEX.match(line)
		if match is None:
			return

		a = match.group(1)
		return cls(a)

class MulInstruction(UnaryInstruction):
	INSTRUCTION_REGEX = re.compile('mul ([\da-z]+)')

	def execute(self, context):
		multiplier = context.registers[self.a].value
		context.registers['a'].value *= multiplier

	@classmethod
	def parse(cls, line):
		match = cls.INSTRUCTION_REGEX.match(line)
		if match is None:
			return

		a = match.group(1)
		return cls(a)

class OutInstruction(UnaryInstruction):
	INSTRUCTION_REGEX = re.compile('out ([\-\da-z]+)')

	def execute(self, context):
		value = self.get_operand_value(context)
		context.clock_signal.append(value)

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
		return cls(a)

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