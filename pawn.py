from piece import Piece
from square import Square
from color import Color
from bishop import Bishop
from rook import Rook 
from knight import Knight 
from queen import Queen

class Pawn(Piece):
	def __init__(self, color, square):
		super().__init__(color, square)
		self.img = 'P' if not color.value else 'p'

	def __str__(self):
		return super().__str__()

	def can_double_move(self, sq):
		x, y = Square.get_square_difference(self.square, sq)
		if x != 0 or not self.is_first_move:
			return False
		if self.color == Color.WHITE:
			return self.square.y + 2 == sq.y
		else:
			return self.square.y - 2 == sq.y

	def can_move(self, sq):
		if self.can_double_move(sq):
			return True
		x, y = Square.get_square_difference(self.square, sq)
		if x != 0:
			return False
		if self.color == Color.WHITE:
			return self.square.y + 1 == sq.y
		else:
			return self.square.y - 1 == sq.y

	def can_take(self, sq):
		x, y = Square.get_square_difference(self.square, sq)
		if x != 1:
			return False
		if self.color == Color.WHITE:
			return self.square.y + 1 == sq.y
		else:
			return self.square.y - 1 == sq.y

	@staticmethod
	def get_path(sq1, sq2):
		if abs(sq1.y - sq2.y) == 2:
			return [Square(sq1.x, (sq1.y + sq2.y) // 2), sq2]
		else:
			return [sq2]

	@staticmethod
	def ask_promotion(color, sq):
		piece = input("Choose promotion\n").lower()
		if piece == 'bishop':
			return Bishop(color, sq)
		if piece == 'knight':
			return Knight(color, sq)
		if piece == 'rook':
			return Rook(color, sq)
		if piece == 'queen':
			return Queen(color, sq)