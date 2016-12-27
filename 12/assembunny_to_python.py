"""
Write your Assembunny in Python,
you'll get the answer much quicker.
"""

import sys
import re

class Instruction(object):
	"""Represents an Assembunny instruction."""
	def __init__(self, line):
		self.line = line

	def __repr__(self):
		return '<%s [%s]>' % (
			self.__class__.__name__,
			self.line)

	def to_python(self):
		raise NotImplementedError()

	@classmethod
	def parse(cls, line):
		raise NotImplementedError()

class UnaryInstruction(Instruction):
	def __init__(self, line, a):
		super(UnaryInstruction, self).__init__(line)
		self.a = a

class BinaryInstruction(Instruction):
	def __init__(self, line, a, b):
		super(BinaryInstruction, self).__init__(line)
		self.a = a
		self.b = b

class CpyInstruction(BinaryInstruction):
	INSTRUCTION_REGEX = re.compile('cpy ([\da-z]+) ([\da-z]+)')

	def to_python(self):
		return '%s = %s' % (
			self.b,
			self.a)

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
		return cls(line, a, b)

class IncInstruction(UnaryInstruction):
	INSTRUCTION_REGEX = re.compile('inc ([\da-z]+)')

	def to_python(self):
		return '%s += 1' % (self.a)

	@classmethod
	def parse(cls, line):
		match = cls.INSTRUCTION_REGEX.match(line)
		if match is None:
			return

		a = match.group(1)
		return cls(line, a)

class DecInstruction(UnaryInstruction):
	INSTRUCTION_REGEX = re.compile('dec ([\da-z]+)')

	def to_python(self):
		return '%s -= 1' % (self.a)

	@classmethod
	def parse(cls, line):
		match = cls.INSTRUCTION_REGEX.match(line)
		if match is None:
			return

		a = match.group(1)
		return cls(line, a)

class JnzInstruction(BinaryInstruction):
	INSTRUCTION_REGEX = re.compile('jnz ([\-\da-z]+) ([\-\d]+)')

	def to_python(self):
		offset = self.b
		if offset > 0:
			line = 'if (%s != 0):' % (self.a)
		elif offset < 0:
			line = 'while (%s != 0):' % (self.a)
		else:
			raise ValueError('Invalid jump offset')
		return line

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
		return cls(line, a, b)

INSTRUCTION_SET = [
	CpyInstruction,
	IncInstruction,
	DecInstruction,
	JnzInstruction,
]

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

def collect_variables(instructions):
	names = set()
	for instruction in instructions:
		a = getattr(instruction, 'a', None)
		if a is not None and isinstance(a, str):
			names.add(a)
		b = getattr(instruction, 'b', None)
		if b is not None and isinstance(b, str):
			names.add(b)
	return sorted(names)

def init_variables(names):
	output = ''
	for name in names:
		output += '%s = 0\n' % (name)
	return output

def convert_instructions(instructions, indentation_level=0):
	output = ''
	i = 0
	while i < len(instructions):
		instruction = instructions[i]
		indentation = '\t' * indentation_level
		output += '%s%s\n' % (
			indentation,
			instruction.to_python())
		if isinstance(instruction, JnzInstruction):
			offset = abs(instruction.b)
			output += convert_instructions(
				instructions[i + 1: i + offset + 1],
				indentation_level + 1)
			i += offset
		i += 1
	return output

def print_variables(names):
	output = ''
	for name in names:
		output += 'print "%s = %%d" %% (%s)\n' % (
			name,
			name)
	return output

def reorder_instructions(instructions):
	# First, reorder jump instructions.
	# Jumps with negative offsets are placed in the 
	# according index in the list.
	reordered_instructions = instructions[:]
	for i, instruction in enumerate(instructions):
		if not isinstance(instruction, JnzInstruction):
			continue
		offset = instruction.b
		if offset > 0:
			continue
		reordered_instructions.pop(i)
		reordered_instructions.insert(
			i + offset,
			instruction)
	return reordered_instructions

def assembunny_to_python(lines):
	instructions = parse_instruction_lines(
		lines,
		INSTRUCTION_SET)
	reordered_instructions = reorder_instructions(
		instructions)
	names = collect_variables(instructions)

	output = init_variables(names)
	output += convert_instructions(reordered_instructions)
	output += print_variables(names)
	return output

def main():
	input_path = sys.argv[1]
	output_path = input_path + '.py'

	data = open(input_path, 'r').read()
	lines = data.split('\n')[:-1]

	script = assembunny_to_python(lines)
	open(output_path, 'wb').write(script)

if __name__ == '__main__':
	main()