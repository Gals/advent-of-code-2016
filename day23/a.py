import sys
import re

from assembunny import *

class KeypadExecutionContext(ExecutionContext):
	def execute(self):
		while self.instruction_pointer < len(self.stack):
			next_instruction = self.stack[self.instruction_pointer]
			try:
				next_instruction.execute(self)
			except InvalidInstructionError:
				print 'Invalid instruction: %r' % (next_instruction)
			self.instruction_pointer += 1
			print self

def resolve_name_conflict(name, names):
	new_name = name
	tries = 0
	while new_name in names:
		tries += 1
		new_name = '%s%d' % (name, tries)
	return new_name

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

	return KeypadExecutionContext(
		registers=registers,
		stack=stack)

INSTRUCTION_SET = [
	CpyInstruction,
	IncInstruction,
	DecInstruction,
	JnzInstruction,
	TglInstruction
]

def test():
	instruction_lines = [
		'cpy 2 a',
		'tgl a',
		'tgl a',
		'tgl a',
		'cpy 1 a',
		'dec a',
		'dec a',
	]
	stack = parse_instruction_lines(
		instruction_lines,
		INSTRUCTION_SET)
	context = execution_context_factory(
		registers_number=4,
		stack=stack)
	
	print context
	context.execute()
	print context.registers['a'].value
	assert context.registers['a'].value == 3

def main():
	# test()
	
	data = open(sys.argv[1], 'r').read()
	instruction_lines = data.split('\n')[:-1]
	stack = parse_instruction_lines(
		instruction_lines,
		INSTRUCTION_SET)
	context = execution_context_factory(
		registers_number=4,
		stack=stack)
	context.registers['a'].value = 7
	context.execute()
	print context.registers['a']
	
if __name__ == '__main__':
	main()
