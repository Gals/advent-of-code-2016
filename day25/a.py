import sys
import re

from assembunny import *

class ClockSignalException(Exception):
	pass

class InvalidClockSignalException(ClockSignalException):
	pass

class RepeatingClockSignalException(ClockSignalException):
	pass

class AntennaExecutionContext(ClockSignalExecutionContext):
	pass

class _OutInstruction(OutInstruction):
	def execute(self, context):
		super(_OutInstruction, self).execute(context)
		expected_signal = 0
		for signal in context.clock_signal[:16]:
			if signal != expected_signal:
				raise InvalidClockSignalException()
			expected_signal = int(not expected_signal)
		if len(context.clock_signal) > 16:
			raise RepeatingClockSignalException()

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

	return AntennaExecutionContext(
		registers=registers,
		stack=stack)

INSTRUCTION_SET = [
	CpyInstruction,
	IncInstruction,
	DecInstruction,
	JnzInstruction,
	_OutInstruction,
]

def solve(stack):
	value = 0
	while True:
		context = execution_context_factory(
			registers_number=4,
			stack=stack)
		context.registers['a'].value = value
		try:
			context.execute()
		except InvalidClockSignalException:
			value += 1
			continue
		except RepeatingClockSignalException:
			break
	print value

def main():	
	data = open(sys.argv[1], 'r').read()
	instruction_lines = data.split('\n')[:-1]
	stack = parse_instruction_lines(
		instruction_lines,
		INSTRUCTION_SET)
	solve(stack)
	
if __name__ == '__main__':
	main()
