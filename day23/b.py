import sys
import re
from pprint import pprint

from assembunny import *

class KeypadExecutionContext(ExecutionContext):
	def _optimize_mul(self, body):
		# b = [b] or constant
		# a += b * d
		mul_flow = [
			CpyInstruction,
			IncInstruction,
			DecInstruction,
			JnzInstruction,
			DecInstruction
		]

		if len(body) != len(mul_flow):
			# Could not be optimized into 'mul'.
			return

		for i, instruction in enumerate(body):
			if not isinstance(instruction, mul_flow[i]):
				# Could not be optimized into 'mul'.
				return

		a = body[1].a
		b = body[0].get_first_operand_value(self)
		c = body[0].b
		d = body[4].a
		self.registers[a].value += b * self.registers[d].value
		self.registers[c].value = 0
		self.registers[d].value = 0

	def _optimize_jnz(self, instruction):
		if not isinstance(instruction, JnzInstruction):
			return

		offset = instruction.get_second_operand_value(self)
		if offset >= 0 or not isinstance(instruction.a, str):
			# Not a loop.
			return

		ip = self.instruction_pointer 
		body = self.stack[ip + offset:ip]
		self._optimize_mul(body)

	def _optimize(self, instruction):
		self._optimize_jnz(instruction)

	def execute(self):
		while self.instruction_pointer < len(self.stack):
			instruction = self.stack[self.instruction_pointer]
			self._optimize(instruction)
			try:
				instruction.execute(self)
			except InvalidInstructionError:
				print 'Invalid instruction: %r' % (instruction)			
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
	context.registers['a'].value = 12
	context.execute()
	print context.registers['a']
	
if __name__ == '__main__':
	main()
