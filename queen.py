from piece import Piece 
from square import Square
from bishop import Bishop
from rook import Rook


class Queen(Piece):
	def __init__(self, color, square):
		super().__init__(color, square)
		self.img = 'Q' if not color.value else 'q'

	def __str__(self):
		return super().__str__()

	def can_move(self, sq):
		x, y = Square.get_square_difference(self.square, sq)
		return x + y > 0 and (x * y == 0 or x == y)

	def get_path(self, sq2):
		return self.__class__.get_path(self.square, sq2)

	@staticmethod
	def get_path(sq1, sq2):
		x, y = Square.get_square_difference(sq1, sq2)
		if x == y:
			return Bishop.get_path(sq1, sq2)
		return Rook.get_path(sq1, sq2)

