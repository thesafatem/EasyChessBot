from piece import Piece 
from square import Square

class Bishop(Piece):
	def __init__(self, color, square):
		super().__init__(color, square)
		self.img = 'B' if not color.value else 'b'

	def __str__(self):
		return super().__str__()

	def can_move(self, sq):
		x, y = Square.get_square_difference(self.square, sq)
		return x == y and x > 0

	@staticmethod
	def get_path(sq1, sq2):
		path = []
		sx = "abcdefgh"
		sy = [i for i in range(1, 9)]
		if sq1.get_x() > sq2.get_x():
			sx = sx[::-1]
		if sq1.y > sq2.y:
			sy = sy[::-1]
		x = sx.index(sq1.x) + 1
		y = sy.index(sq1.y) + 1
		while x <= sx.index(sq2.x):
			path.append(Square(sx[x], sy[y]))
			x += 1
			y += 1
		return path
