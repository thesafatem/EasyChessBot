from piece import Piece 
from square import Square

class Knight(Piece):
	def __init__(self, color, square):
		super().__init__(color, square)
		self.img = 'N' if not color.value else 'n'

	def __str__(self):
		return super().__str__()

	def can_move(self, sq):
		x, y = Square.get_square_difference(self.square, sq)
		return (x == 2 and y == 1) or (x == 1 and y == 2)

	@staticmethod
	def get_path(sq1, sq2):
		return [sq2]