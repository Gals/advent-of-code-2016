import sys
import re

def contains_abba(string):
	for i in xrange(len(string) - 3):
		# The characters have to be different.
		if string[i] == string[i + 1]:
			continue
		first_half = string[i:i + 2]
		second_half = string[i + 2:i + 4]
		if first_half == second_half[::-1]:
			return True
	return False

def supports_tls(ip_address):
	# Substrings within square brackets should not contain ABBA.
	for within_brackets in re.findall('\[(.+?)\]', ip_address):
		if contains_abba(within_brackets):
			return False
	
	# Remove brackets from the ip address.
	parts_without_brackets = re.sub('\[(.+?)\]', ',', ip_address).split(',')
	for part in parts_without_brackets:
		if contains_abba(part):
			return True
	return False

def main():
	# ip_addresses = [
	# 	'abba[mnop]qrst',
	# 	'abcd[bddb]xyyx',
	# 	'aaaa[qwer]tyui',
	# 	'ioxxoj[asdfgh]zxcvbn',
	# ]
	ip_addresses = open(sys.argv[1], 'r').read().split('\n')[:-1]

	support_tls_count = 0
	for ip_address in ip_addresses:
		if supports_tls(ip_address):
			support_tls_count += 1
			print 'Supports TLS: %r' % (ip_address)
		else:
			print 'Does not support TLS: %r' % (ip_address)
	print 'Support TLS: %d (out of %d)' % (
		support_tls_count,
		len(ip_addresses))

if __name__ == '__main__':
	main()