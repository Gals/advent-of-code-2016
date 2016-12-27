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

def find_shortest_path(src, dst, favorite_number):
	queue = [(0, src)]
	visited_points = []
	distances = []

	while len(queue) > 0:
		distance, p = queue.pop(0)
		if p.x == dst.x and p.y == dst.y:
			distances.append(distance)
			continue

		offsets = [(1, 0), (0, 1), (-1, 0), (0, -1)]
		for (offset_x, offset_y) in offsets:
			neighbour = Point(p.x + offset_x, p.y + offset_y)
			if neighbour.x < 0 or neighbour.y < 0:
				# Skip invalid points.
				continue
			if point_in_list(neighbour, visited_points):
				# Avoid loops.
				continue
			if is_wall(neighbour, favorite_number):
				continue
			queue.append((distance + 1, neighbour))
			visited_points.append(neighbour)

	return min(distances)

# def find_shortest_path(src, dst, favorite_number, 
# 	path=None, paths=None):
# 	path = path or []
# 	paths = paths or []

# 	if src.x == dst.x and src.y == dst.y:
# 		paths.append(len(path))
# 		# We've reached our destination.
# 		return min(paths)

# 	neighbours_paths = []
# 	offsets = [(1, 0), (0, 1), (-1, 0), (0, -1)]
# 	for (offset_x, offset_y) in offsets:
# 		neighbour = Point(src.x + offset_x, src.y + offset_y)
# 		if neighbour.x < 0 or neighbour.y < 0:
# 			# Skip invalid points.
# 			continue
# 		if point_in_path(neighbour, path):
# 			# Avoid loops.
# 			continue
# 		if is_wall(neighbour, favorite_number):
# 			# Hitting a wall.
# 			continue
# 		shortest_path = find_shortest_path(
# 			neighbour,
# 			dst,
# 			favorite_number,
# 			path + [neighbour],
# 			paths)
# 		if shortest_path == -1:
# 			continue
# 		neighbours_paths.append(shortest_path)

# 	if len(neighbours_paths) == 0:
# 		return -1

# 	return min(neighbours_paths)

def main():
	favorite_number = int(sys.argv[1])
	start_point = Point(1, 1)
	end_point = Point(31, 39)

	print find_shortest_path(
		start_point,
		end_point,
		favorite_number)

if __name__ == '__main__':
	main()