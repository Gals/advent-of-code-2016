# Taken from adventofcode solution:
# https://www.reddit.com/r/adventofcode/comments/5j4lp1/2016_day_19_solutions/dbdf9go/
import sys

class Node(object):
	def __init__(self, number):
		self.number = number
		self.previous = None
		self.next = None

	def delete(self):
		self.previous.next = self.next
		self.next.previous = self.previous

def solve(elves):
	l = [Node(i) for i in xrange(elves)]
	for i, n in enumerate(l):
		n.next = l[(i + 1) % len(l)]
		n.previous = l[(i - 1) % len(l)]

	start = l[0]
	middle = l[elves / 2]

	for i in xrange(elves - 1):
		middle.delete()
		middle = middle.next
		if (elves - i) % 2 == 1:
			middle = middle.next
		start = start.next

	return start.number + 1

def test():
	assert solve(5) == 2

def main():
	# test()
	print solve(3005290)

if __name__ == '__main__':
	main()