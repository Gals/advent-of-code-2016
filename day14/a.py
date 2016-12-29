import sys
import hashlib
import re

def get_hash(salt, index=0):
	data = '%s%d' % (salt, index)
	return hashlib.md5(data).hexdigest()

def get_triplet_character(s):
	triplet_regex = re.compile(r'(.)\1\1')
	match = triplet_regex.search(s)
	if match:
		return match.group(1)

def contains_five_sequence(c, hashes):
	for current_hash in hashes:
		if c * 5 in current_hash:
			return True
	return False

def get_key_index(salt, key):
	hashes = [get_hash(salt, x) for x in range(1000)]

	i = 0
	keys_found = 0

	while True:
		c = get_triplet_character(hashes.pop(0))
		if c and contains_five_sequence(c, hashes):
			keys_found += 1
			if keys_found == key:
				break

		i += 1
		hashes.append(get_hash(salt, i + len(hashes)))

	return i

def main():
	print get_key_index(sys.argv[1], 64)

if __name__ == '__main__':
	main()