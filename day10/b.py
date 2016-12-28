import sys
import re

class OutputBin(object):
	def __init__(self, name, chips=None):
		self.name = name
		self.chips = chips or []

	def __repr__(self):
		return '<%s [%s]>' % (
			self.__class__.__name__,
			self.name)

	def add_chip(self, value):
		self.chips.append(value)
		self.chips = sorted(self.chips)

class Bot(object):
	def __init__(self, name, chips=None):
		self.name = name
		self.chips = chips or []

	def __repr__(self):
		return '<%s [%s]>' % (
			self.__class__.__name__,
			self.name)

	def add_chip(self, value):
		self.chips.append(value)
		self.chips = sorted(self.chips)

	def hand_low_chip(self):
		return self.chips.pop(0)

	def hand_high_chip(self):
		return self.chips.pop(len(self.chips) - 1)

class InstructionExecutionFailedError(Exception):
	pass

class Instruction(object):
	def execute(self, bots, output_bins):
		raise NotImplementedError()

	@classmethod
	def parse(cls, line):
		raise NotImplementedError()

class ValueGoesToInstruction(Instruction):
	INSTRUCTION_REGEX = re.compile('value (\d+) goes to bot (\d+)')

	def __init__(self, chip_value, bot_name):
		self.chip_value = chip_value
		self.bot_name = bot_name

	def execute(self, bots, output_bins):
		bots.setdefault(self.bot_name, Bot(self.bot_name))
		bots[self.bot_name].add_chip(self.chip_value)

	@classmethod
	def parse(cls, line):
		match = cls.INSTRUCTION_REGEX.match(line)
		if not match:
			return

		chip_value = int(match.group(1))
		bot_name = match.group(2)
		return cls(chip_value, bot_name)

class ChipDestinationTypes:
	BOT = 'bot'
	OUTPUT = 'output'
	ALL = [BOT, OUTPUT]

class GivesLowToAndHighToInstruction(Instruction):
	INSTRUCTION_REGEX = re.compile(
		'bot (\d+) gives low to (%(types)s) (\d+) and high to (%(types)s) (\d+)' % dict(
			types='|'.join(ChipDestinationTypes.ALL)))

	def __init__(self, bot_name, 
		low_dest_type, low_dest_name, 
		high_dest_type, high_dest_name):
		self.bot_name = bot_name
		self.low_dest_type = low_dest_type
		self.low_dest_name = low_dest_name
		self.high_dest_type = high_dest_type
		self.high_dest_name = high_dest_name

	def add_chip_to_bot(self, bots, name, value):
		bots.setdefault(name, Bot(name))
		bots[name].add_chip(value)

	def add_chip_to_output(self, output_bins, name, value):
		output_bins.setdefault(name, OutputBin(name))
		output_bins[name].add_chip(value)

	def execute(self, bots, output_bins):
		bot = bots.get(self.bot_name)
		if bot is None:
			raise InstructionExecutionFailedError(
				'Bot %r does not exist' % (self.bot_name))

		if len(bot.chips) < 2:
			raise InstructionExecutionFailedError(
				'Bot %r does not have 2 chips' % (bot.name))

		low = bot.hand_low_chip()
		if self.low_dest_type == ChipDestinationTypes.BOT:
			self.add_chip_to_bot(
				bots, self.low_dest_name, low)
		elif self.low_dest_type == ChipDestinationTypes.OUTPUT:
			self.add_chip_to_output(
				output_bins, self.low_dest_name, low)

		high = bot.hand_high_chip()
		if self.high_dest_type == ChipDestinationTypes.BOT:
			self.add_chip_to_bot(
				bots, self.high_dest_name, high)
		elif self.high_dest_type == ChipDestinationTypes.OUTPUT:
			self.add_chip_to_output(
				output_bins, self.high_dest_name, high)

	@classmethod
	def parse(cls, line):
		match = cls.INSTRUCTION_REGEX.match(line)
		if not match:
			return

		bot_name = match.group(1)

		low_dest_type = match.group(2)
		low_dest_name = match.group(3)

		high_dest_type = match.group(4)
		high_dest_name = match.group(5)
		return cls(
			bot_name,
			low_dest_type,
			low_dest_name,
			high_dest_type,
			high_dest_name)

INSTRUCTION_SET = [
	ValueGoesToInstruction,
	GivesLowToAndHighToInstruction,
]

def sort_instructions(instruction_set, lines):
	sorted_lines = []
	first_lines = []
	other_lines = []
	for line in lines:
		if ValueGoesToInstruction.parse(line):
			first_lines.append(line)
		else:
			other_lines.append(line)
	sorted_lines = first_lines
	sorted_lines.extend(other_lines)
	return sorted_lines

def execute_instruction(instruction_set, line, 
	bots, output_bins):
	for instruction_class in instruction_set:
		instruction = instruction_class.parse(line)
		if not instruction:
			continue
		instruction.execute(bots, output_bins)

def main():
	instructions = open(sys.argv[1], 'r').read().split('\n')[:-1]
	instructions = sort_instructions(
		INSTRUCTION_SET,
		instructions)
	bots = {}
	output_bins = {}

	while instructions:
		instruction = instructions.pop(0)
		print instruction

		try:
			execute_instruction(
				INSTRUCTION_SET,
				instruction,
				bots,
				output_bins)
		except InstructionExecutionFailedError, e:
			print e
			# Push to the end of the instructions queue.
			instructions.append(instruction)
			continue

	for name, output_bin in output_bins.items():
		print output_bin
		print output_bin.chips

	product = 1
	requested_output_bins = ['0', '1', '2']
	for name in requested_output_bins:
		product *= output_bins[name].chips[0]
	print 'Output bins %r product: %d' % (
		requested_output_bins,
		product)

if __name__ == '__main__':
	main()