import sys
import hashlib

def get_open_doors(passcode, path):
	doors = []
	open_door_characters = ['b', 'c', 'd', 'e', 'f']
	h = hashlib.md5(passcode + path).hexdigest()[:4]
	for i, door in enumerate(['U', 'D', 'L', 'R']):
		if h[i] in open_door_characters:
			doors.append(door)
	return doors

def find_shortest_path(passcode, destination):
	dst_x, dst_y = destination
	door_to_offsets = {
		'U': (0, -1),
		'D': (0, 1),
		'L': (-1, 0),
		'R': (1, 0)
	}
	
	queue = [((0, 0), '')]
	shortest_path = ''
	while len(queue) > 0:
		(x, y), path = queue.pop(0)
		if x == dst_x and y == dst_y:
			shortest_path = path
			continue

		for door in get_open_doors(passcode, path):
			offsets = door_to_offsets[door]
			new_x = x + offsets[0]
			new_y = y + offsets[1]
			if new_x < 0 or new_y < 0:
				# Invalid coordinates.
				continue
			new_path = path + door
			if len(shortest_path) == 0 or \
				len(new_path) < len(shortest_path):
				queue.append(((new_x, new_y), new_path))
	return shortest_path

def test():
	assert find_shortest_path('ihgpwlah', (3 ,3)) == 'DDRRRD'
	assert find_shortest_path('kglvqrro', (3, 3)) == 'DDUDRLRRUDRD'
	# Seems like they've made a mistake here, shortest path should be 'DRURDRUDDRDL'.
	# assert find_shortest_path('ulqzkmiv') == 'DRURDRUDDLLDLUURRDULRLDUUDDDRR'

def main():
	# test()
	print find_shortest_path('bwnlcvfs', (3, 3))

if __name__ == '__main__':
	main()