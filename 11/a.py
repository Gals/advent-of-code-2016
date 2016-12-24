import time
import itertools
import copy

class Component(object):
	def __init__(self, element):
		self.element = element

	def __repr__(self):
		return '<%s [%s]>' % (
			self.__class__.__name__,
			self.element)

class Generator(Component):
	pass

class Microchip(Component):
	pass

class Floor(object):
	def __init__(self, number, components=None):
		self.number = number
		self.components = components or []

	def __repr__(self):
		return '<%s [%d]>' % (
			self.__class__.__name__,
			self.number)

class State(object):
	def __init__(self, elevator, floors, moves=1):
		self.elevator = elevator
		self.floors = floors
		self.moves = moves
		self._floors_hash = None
		self._hash = None

	def __repr__(self):
		return '<%s [%d, %s, %d]>' % (
			self.__class__.__name__,
			self.elevator,
			self.floors,
			self.moves)

	@property
	def hash(self):
		"""A good hash is a key. It saves you visiting in states that
		you've already seen, and visting equivalent states."""
		if self._hash is not None:
			return self._hash
		
		# We can represent the floors hash as a list of the number of components 
		# in each floor, because we're calculating only the hashes of valid states.
		floors_hash = str([len(f.components) for f in self.floors])
		self._hash = str(self.elevator) + '|' + floors_hash
		return self._hash

class Elements:
	HYDROGEN = 1
	LITHIUM = 2
	THULIUM	= 3
	PLUTONIUM = 4
	STRONTIUM = 5
	PROMETHIUM = 6
	RUTHENIUM = 7
	ELERIUM = 8
	DILITHIUM = 9

def visit_state(state, visited_states):
	visited_states.add(state.hash)

def visited_state(state, visited_states):
	return state.hash in visited_states

def move_component(component, src_floor, dst_floor):
	if component not in src_floor.components:
		print component
		print src_floor.components
		import pdb;pdb.set_trace()
	src_floor.components.remove(component)
	dst_floor.components.append(component)

def has_matching_generator(microchip, floor):
	return -microchip in floor.components

def is_valid_state(floor):
	contains_generators = False
	unpaired = False
	for component in floor.components:
		if component < 0:
			contains_generators = True
			continue
		if not has_matching_generator(component, floor):
			unpaired = True
			break
	if unpaired and contains_generators:
		return False
	return True

def create_new_states(elevator, floors, 
	components_to_move, src_floor_number, dst_floor_number):
	new_states = []
	for (a, b) in components_to_move:
		new_floors = copy.deepcopy(floors)
		src_floor = new_floors[src_floor_number - 1]
		dst_floor = new_floors[dst_floor_number - 1]

		new_state = State(
			elevator=elevator,
			floors=new_floors)

		move_component(a, src_floor, dst_floor)
		if b is not None:
			move_component(b, src_floor, dst_floor)
		if is_valid_state(src_floor) and is_valid_state(dst_floor):
			new_states.append(new_state)

	return new_states

def get_child_states_going_up(state):
	current_floor = state.floors[state.elevator - 1]
	floor_above = state.floors[state.elevator]

	# 2 components together.
	components_to_move = []
	for pair in itertools.combinations(current_floor.components, 2):
		components_to_move.append(pair)

	new_states = create_new_states(
		state.elevator + 1,
		state.floors,
		components_to_move,
		current_floor.number,
		floor_above.number)
	if len(new_states) > 0:
		# We can move two components together.
		return new_states

	# The flooor above does not contain any component,
	# there's no point in going upstairs.
	if len(floor_above.components) == 0:
		return []

	# Moving one component at a time.
	components_to_move = []
	for component in current_floor.components:
		components_to_move.append((component, None))

	return create_new_states(
		state.elevator + 1,
		state.floors,
		components_to_move,
		current_floor.number,
		floor_above.number)

def get_child_states_going_down(state):
	current_floor = state.floors[state.elevator - 1]
	floor_below = state.floors[state.elevator - 2]

	# Find the lowest floor containing components.
	lowest_floor = len(state.floors)
	for floor in state.floors:
		if len(floor.components) > 0:
			lowest_floor = min(lowest_floor, floor.number)			

	if lowest_floor > floor_below.number:
		# No point in going downstairs, because there are no
		# components waiting there.
		return []

	components_to_move = []
	for component in current_floor.components:
		components_to_move.append((component, None))

	new_states = create_new_states(
		state.elevator - 1,
		state.floors,
		components_to_move,
		current_floor.number,
		floor_below.number)
	if len(new_states) > 0:
		# We can move one component at a time.
		return new_states

	# 2 components together.
	components_to_move = []
	for pair in itertools.combinations(current_floor.components, 2):
		components_to_move.append(pair)

	return create_new_states(
		state.elevator - 1,
		state.floors,
		components_to_move,
		current_floor.number,
		floor_below.number)

def get_child_states(state):
	if state.elevator == 1:
		# We're going up.
		return get_child_states_going_up(state)

	if state.elevator == len(state.floors):
		# We're going down.
		return get_child_states_going_down(state)

	# Going in both directions.
	return get_child_states_going_up(state) + \
		get_child_states_going_down(state)

def final_state_factory(initial_state):
	floors = copy.deepcopy(initial_state.floors)
	final_state = State(
		elevator=len(floors),
		floors=floors)

	top_floor = final_state.floors[-1]
	for floor in final_state.floors[:-1]:
		top_floor.components.extend(floor.components)
		floor.components = []

	return final_state

def find_shortest_path(initial_state):
	initial_state.moves = 0

	states = [initial_state]
	visited_states = set()
	visit_state(initial_state, visited_states)

	final_state = final_state_factory(initial_state)
	final_state_hash = final_state.hash

	while len(states) > 0:
		state = states.pop(0)
		# print state.hash

		if state.hash == final_state_hash:
			return state.moves

		child_states = get_child_states(state)
		for child_state in child_states:
			# Going deeper.
			child_state.moves = state.moves + 1
			if not visited_state(child_state, visited_states):
				states.append(child_state)
				visit_state(child_state, visited_states)

	return 0

def floor_factory(number, microchips=None, generators=None):
	microchips = microchips or []
	generators = generators or []

	components = []
	for m in microchips:
		components.append(m.element)
	for g in generators:
		components.append(g.element * -1)
	return Floor(number, components)

def main():
	start_time = time.time()

	floor1 = floor_factory(1, microchips=[Microchip(Elements.HYDROGEN), Microchip(Elements.LITHIUM)])
	floor2 = floor_factory(2, generators=[Generator(Elements.HYDROGEN)])
	floor3 = floor_factory(3, generators=[Generator(Elements.LITHIUM)])
	floor4 = floor_factory(4)

	# floor1 = floor_factory(1, 
	# 	[Microchip(Elements.THULIUM)],
	# 	[Generator(Elements.THULIUM), Generator(Elements.PLUTONIUM), Generator(Elements.STRONTIUM)])
	# floor2 = floor_factory(2,
	# 	[Microchip(Elements.PLUTONIUM), Microchip(Elements.STRONTIUM)])
	# floor3 = floor_factory(3,
	# 	[Microchip(Elements.PROMETHIUM), Microchip(Elements.RUTHENIUM)],
	# 	[Generator(Elements.PROMETHIUM), Generator(Elements.RUTHENIUM)])
	# floor4 = floor_factory(4)

	# floor1 = floor_factory(1, 
	# 	[Microchip(Elements.THULIUM), Microchip(Elements.ELERIUM), Microchip(Elements.DILITHIUM)],
	# 	[Generator(Elements.THULIUM), Generator(Elements.PLUTONIUM), Generator(Elements.STRONTIUM), Generator(Elements.ELERIUM), Generator(Elements.DILITHIUM)])
	# floor2 = floor_factory(2,
	# 	[Microchip(Elements.PLUTONIUM), Microchip(Elements.STRONTIUM)])
	# floor3 = floor_factory(3,
	# 	[Microchip(Elements.PROMETHIUM), Microchip(Elements.RUTHENIUM)],
	# 	[Generator(Elements.PROMETHIUM), Generator(Elements.RUTHENIUM)])
	# floor4 = floor_factory(4)

	state = State(
		elevator=1,
		floors=[floor1, floor2, floor3, floor4]
	)
	print find_shortest_path(state)

	end_time = time.time()
	time_elapsed = end_time - start_time
	print 'Took %.2f seconds' % (time_elapsed)

if __name__ == '__main__':
	main()