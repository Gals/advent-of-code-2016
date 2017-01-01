import sys

def solve_trivial(elves):
	players = [[i + 1, 1] for i in xrange(elves)]
	while len(players) > 1:
		for i, player in enumerate(players):
			position, _ = player
			left_player = i + 1 if i + 1 < len(players) else 0
			# Take the presents of the left player.
			players[i][1] += players[left_player][1]
			players.pop(left_player)
	position, _ = players[0]
	return position

def biggest_power_of(a, n):
	m = 1
	while a ** m < n:
		m += 1
	return a ** (m - 1)

def solve(elves):
	"""
	This solution is based on the explanation in this video:
	https://www.youtube.com/watch?v=uCsD3ZGzMgE
	"""
	l = elves - biggest_power_of(2, elves)
	return 2 * l + 1

def test():
	assert solve_trivial(5) == 3
	assert solve(5) == 3
	assert solve(13) == 11
	assert solve(41) == 19

def main():
	# test()
	print solve(3005290)

if __name__ == '__main__':
	main()