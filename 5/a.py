import sys
import hashlib

PASSWORD_LENGTH = 8

def md5(data):
	return hashlib.md5(data).hexdigest()

def get_password_char(door_id, length):
	i = 0
	for _ in xrange(length):
		found = False
		while not found:
			md5_hash = md5('%s%d' % (door_id, i))
			if md5_hash.startswith('00000'):
				char = md5_hash[5]
				yield char
				found = True
			
			i += 1

def main():
	door_id = sys.argv[1]
	
	password = ''
	for c in get_password_char(door_id, PASSWORD_LENGTH):
		password += c
	print 'Password: %r' % (password)

if __name__ == '__main__':
	main()