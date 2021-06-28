from piece import Piece 
from square import Square

class Rook(Piece):
	def __init__(self, color, square):
		super().__init__(color, square)
		self.img = 'R' if not color.value else 'r'

	def __str__(self):
		return super().__str__()

	def can_move(self, sq):
		x, y = Square.get_square_difference(self.square, sq);
		return x * y == 0 and x + y > 0

	@staticmethod
	def get_path(sq1, sq2):
		path = []
		if sq1.get_x() == sq2.get_x():
			s = [i for i in range(1, 9)]
			if sq1.y > sq2.y:
				s = s[::-1]
			for y in range(s.index(sq1.y) + 1, s.index(sq2.y) + 1):
				path.append(Square(sq1.x, s[y]))
		else:
			s = "abcdefgh"
			if sq1.get_x() > sq2.get_x():
				s = s[::-1]
			for x in range(s.index(sq1.x) + 1, s.index(sq2.x) + 1):
				path.append(Square(s[x], sq1.y))
		return path
