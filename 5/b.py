import sys
import hashlib

PASSWORD_LENGTH = 8

def md5(data):
	return hashlib.md5(data).hexdigest()

def get_password_char(door_id, length):
	i = 0
	found_positions = []
	for _ in xrange(length):
		found = False
		while not found:
			md5_hash = md5('%s%d' % (door_id, i))
			if md5_hash.startswith('00000'):
				pos = 0
				try:
					pos = int(md5_hash[5])
				except ValueError:
					i += 1
					continue

				if (pos >= length) or (pos in found_positions):
					# Position is out of range, or the character at 
					# this position is already found, ignore it.
					i += 1
					continue

				found_positions.append(pos)
				char = md5_hash[6]
				yield (pos, char)
				found = True
			i += 1

def main():
	door_id = sys.argv[1]
	
	password = list('_' * PASSWORD_LENGTH)
	for pos, c in get_password_char(door_id, PASSWORD_LENGTH):
		password[pos] = c
		print pos, c
		print ''.join(password)
	print 'Password: %r' % (''.join(password))

if __name__ == '__main__':
	main()