import sys
import re

class Room(object):
	def __init__(self, encrypted_name, sector_id, checksum):
		self.encrypted_name = encrypted_name
		self.sector_id = sector_id
		self.checksum = checksum

	def __repr__(self):
		return '<%s [%r]>' % (
			self.__class__.__name__,
			self.encrypted_name)

def parse_room_data(data):
	room_match = re.match('([a-z\-]+)-(\d+)\[([a-z]+)\]', data)
	if room_match is None:
		return None

	encrypted_name = room_match.group(1)
	sector_id = int(room_match.group(2))
	checksum = room_match.group(3)
	return Room(
		encrypted_name=encrypted_name,
		sector_id=sector_id,
		checksum=checksum)

def parse_rooms_file(file_path):
	rooms = []
	with open(file_path, 'r') as rooms_file:
		for line in rooms_file:
			room = parse_room_data(line)
			if not room:
				continue
			rooms.append(room)
	return rooms

def count_letters(string):
	letters = {}
	for l in string:
		if letters.has_key(l):
			letters[l] += 1
		else:
			letters[l] = 1
	return letters

def calculate_checksum(name):
	letters_count = count_letters(name)
	def checksum_letters_compare(a, b):
		if letters_count[a] == letters_count[b]:
			return ord(b) - ord(a)
		return letters_count[a] - letters_count[b]

	return ''.join(sorted(
		letters_count,
		reverse=True,
		cmp=checksum_letters_compare)[:5])

def is_real_room(room):
	checksum = calculate_checksum(
		room.encrypted_name.replace('-', ''))
	return (checksum == room.checksum)

def decrypt_shift_chiper(m, rotations=1):
	alphabet_size = ord('z') - ord('a') + 1

	decrypted = ''
	m = m.replace('-', ' ')
	for c in m:
		if c == ' ':
			decrypted += ' '
			continue
		if 'a' > c or 'z' < c:
			continue
		for _ in xrange(rotations):
			c = chr(ord('a') + ((ord(c) - ord('a') + 1) % alphabet_size))
		decrypted += c
	return decrypted

def decrypt_room_name(room):
	return decrypt_shift_chiper(room.encrypted_name, 
		rotations=room.sector_id)

def main():
	# print decrypt_room_name(
	# 	Room('qzmt-zixmtkozy-ivhz', 343, ''))

	rooms = parse_rooms_file(sys.argv[1])
	real_rooms = filter(is_real_room, rooms)
	for room in real_rooms:
		name = decrypt_room_name(room)
		print '%r' % (name)
		if 'North'.lower() in name:
			print 'Sector ID: %d' % (room.sector_id)
			break

if __name__ == '__main__':
	main()