import sys

def dragon_curve(data):
	a = data
	b = data[::-1]
	b = b.replace('0', 'x')
	b = b.replace('1', '0')
	b = b.replace('x', '1')
	return '%s0%s' % (a, b)

def test_dragon_curve():
	assert dragon_curve('1') == '100'
	assert dragon_curve('0') == '001'
	assert dragon_curve('11111') == '11111000000'
	assert dragon_curve('111100001010') == '1111000010100101011110000'

def checksum(data):
	while True:
		checksum = ''
		for i in xrange(0, len(data) - 1, 2):
			pair = data[i:i + 2]
			if pair in ['11', '00']:
				checksum += '1'
			else:
				checksum += '0'
		if len(checksum) % 2 == 1:
			break
		data = checksum
	return checksum

def test_checksum():
	assert checksum('110010110100') == '100'

def fill_disk(initial_data, length):
	data = initial_data
	while len(data) < length:
		data = dragon_curve(data)
	data = data[:length]
	return checksum(data)

def test_fill_disk():
	assert fill_disk('10000', 20) == '01100'

def main():
	# test_dragon_curve()
	# test_checksum()
	# test_fill_disk()
	print fill_disk('10001001100000001', 272)
	print fill_disk('10001001100000001', 35651584)
	
if __name__ == '__main__':
	main()