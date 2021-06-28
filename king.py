from piece import Piece
from square import Square

class King(Piece):
	def __init__(self, color, square):
		super().__init__(color, square)
		self.img = 'K' if not color.value else 'k'

	def __str__(self):
		return super().__str__()

	def can_move(self, sq):
		x, y = Square.get_square_difference(self.square, sq)
		return x <= 1 and y <= 1 and x + y > 0

	@staticmethod
	def get_path(sq1, sq2):
		return [sq2]