import sys

def is_wall(p, favorite_number):
	x = p.x
	y = p.y

	result = x * x + 3 * x + 2 * x * y + y + y * y	
	result += favorite_number 
	binary = '{0:b}'.format(result)
	return binary.count('1') % 2 == 1

class Point(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __repr__(self):
		return '<%s (%d, %d)>' % (
			self.__class__.__name__,
			self.x,
			self.y)

def point_in_list(p, points):
	for point in points:
		if p.x == point.x and p.y == point.y:
			return True
	return False

def count_distinct_points(src, max_distance, favorite_number):
	queue = [(0, src)]
	visited = []

	while len(queue) > 0:
		step, p = queue.pop(0)
		if step == max_distance:
			break


		offsets = [(1, 0), (0, 1), (-1, 0), (0, -1)]
		for (offset_x, offset_y) in offsets:
			neighbour = Point(p.x + offset_x, p.y + offset_y)
			if neighbour.x < 0 or neighbour.y < 0:
				# Skip invalid points.
				continue
			if point_in_list(neighbour, visited):
				# Avoid loops.
				continue
			if is_wall(neighbour, favorite_number):
				continue
			queue.append((step + 1, neighbour))
			visited.append(neighbour)

	return len(visited)

def main():
	favorite_number = int(sys.argv[1])
	start_point = Point(1, 1)

	print count_distinct_points(
		start_point,
		50,
		favorite_number)

if __name__ == '__main__':
	main()