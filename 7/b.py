import sys
import re

def list_aba_sequences(string):
	sequences = []
	for i in xrange(len(string) - 2):
		if (string[i] != string[i + 1]) and \
			(string[i] == string[i + 2]):
			sequences.append(string[i:i + 3])
	return sequences

def contains_bab(string, aba_sequence):
	a = aba_sequence[0]
	b = aba_sequence[1]
	expected_bab = ''.join([b, a, b])

	for i in xrange(len(string) - 2):
		if string[i:i + 3] == expected_bab:
			return True
	return False

def supports_ssl(ip_address):
	aba_sequences = set()
	supernet_sequences = re.sub('\[(.+?)\]', ',', ip_address).split(',')
	for supernet_sequence in supernet_sequences:
		aba_sequences.update(
			list_aba_sequences(supernet_sequence))

	if not aba_sequences:
		return False

	hypernet_sequences =  re.findall('\[(.+?)\]', ip_address)
	for aba_sequence in aba_sequences:
		for hypernet_sequence in hypernet_sequences:
			if contains_bab(hypernet_sequence, aba_sequence):
				return True

	return False

def main():
	# ip_addresses = [
	# 	'aba[bab]xyz',
	# 	'xyx[xyx]xyx',
	# 	'aaa[kek]eke',
	# 	'zazbz[bzb]cdb',
	# ]
	ip_addresses = open(sys.argv[1], 'r').read().split('\n')[:-1]

	support_ssl_count = 0
	for ip_address in ip_addresses:
		if supports_ssl(ip_address):
			support_ssl_count += 1
			print 'Supports SSL: %r' % (ip_address)
		else:
			print 'Does not support SSL: %r' % (ip_address)

	print 'Support SSL: %d (out of %d)' % (
		support_ssl_count,
		len(ip_addresses))

if __name__ == '__main__':
	main()