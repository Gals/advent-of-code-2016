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

def find_longest_path(passcode, destination):
	dst_x, dst_y = destination
	door_to_offsets = {
		'U': (0, -1),
		'D': (0, 1),
		'L': (-1, 0),
		'R': (1, 0)
	}
	
	queue = [((0, 0), '')]
	longest_path = ''
	while len(queue) > 0:
		(x, y), path = queue.pop()
		if x == dst_y and y == dst_y:
			if len(path) > len(longest_path):
				longest_path = path
			continue

		for door in get_open_doors(passcode, path):
			offsets = door_to_offsets[door]
			new_x = x + offsets[0]
			new_y = y + offsets[1]
			if new_x < 0 or new_y < 0 or \
				new_x > dst_x or new_y > dst_y:
				# Invalid coordinates.
				continue
			queue.append(((new_x, new_y), path + door))
	return longest_path

def test():
	assert len(find_longest_path('ihgpwlah', (3, 3))) == 370

def main():
	# test()
	print len(find_longest_path('bwnlcvfs', (3, 3)))

if __name__ == '__main__':
	main()