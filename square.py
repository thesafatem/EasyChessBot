class Square:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __str__(self):
		return self.x + str(self.y)

	def __eq__(self, obj):
		return self.x == obj.x and self.y == obj.y

	def __hash__(self):
		return hash((self.x, self.y))

	def get_x(self):
		return ord(self.x) - ord('a') + 1

	@staticmethod
	def get_square_difference(sq1, sq2):
		x = abs(sq1.get_x() - sq2.get_x())
		y = abs(sq1.y - sq2.y)
		return x, y