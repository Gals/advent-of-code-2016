import sys
import re

def expand_range(a, b):
	if a[0] <= b[0] and a[1] >= b[0]:
		return (a[0], max(a[1], b[1]))
	return a

def in_range(a, b):
	return (a[0] > b[0] and a[1] < b[1])

def expand_range_list(l):
	expanded = []
	queue = sorted(l, cmp=lambda x, y: cmp(x[0], y[0]))
	while len(queue) > 0:
		current_range = queue.pop(0)
		expanded_range = current_range
		for unseen_range in queue:
			expanded_range = expand_range(current_range, unseen_range)
			if expanded_range != current_range:
				queue.remove(unseen_range)
				break
			if in_range(unseen_range, expanded_range):
				queue.remove(unseen_range)
		if expanded_range not in expanded:
			expanded.append(expanded_range)
	return expanded

def solve(blacklist):
	expanded_list = []

	expanded = blacklist[:]
	while True:
		new = expand_range_list(expanded)
		if new == expanded:
			break
		expanded = new

	i = 0
	while (i + 1 < len(expanded) and \
		expanded[i][1] + 1 == expanded[i + 1][0]):
		i += 1

	return expanded[i][1] + 1

def test():
	assert expand_range((4, 7), (5, 8)) == (4, 8)
	assert expand_range((0, 2), (4, 7)) == (0, 2)
	assert expand_range((1847081, 6381735), (2642830, 5721362)) == (1847081, 6381735) 
	assert expand_range((1847081, 6381735), (2642830, 12610188)) == (1847081, 12610188)
	assert expand_range((1847081, 12610188), (5553473, 5721362)) == (1847081, 12610188)
	assert expand_range((1847081, 12610188), (6381736, 6572278)) == (1847081, 12610188)
	assert solve([(5, 8), (0, 2), (4, 7)]) == 3

def main():
	test()
	ip_range_regex = re.compile('(\d+)-(\d+)')
	blacklist = []
	with open(sys.argv[1], 'r') as f:
		for line in f:
			match = ip_range_regex.match(line)
			if match is None:
				continue
			low = int(match.group(1))
			high = int(match.group(2))
			blacklist.append((low, high))
	print solve(blacklist)

if __name__ == '__main__':
	main()