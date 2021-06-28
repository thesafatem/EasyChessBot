from color import Color
from square import Square

class Piece:
	def __init__(self, color, square):
		self.color = color
		self.square = square
		self.is_first_move = True
		self.image = self.color.__str__() + "_" + self.__class__.__name__.lower() + '.png'

	def __str__(self):
		return f"{self.color.__str__()} {self.__class__.__name__.lower()} at {self.square.__str__()}"

	def can_move(self, sq):
		pass

	def can_take(self, sq):
		return self.can_move(sq)

	@staticmethod
	def get_path(sq1, sq2):
		pass