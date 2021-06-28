from enum import Enum
from square import Square
from color import Color

class Castling(Enum):
	KINGSIDE = 2
	QUEENSIDE = 3

	def get_path(self, color):
		path = []
		y = 1
		s = 'abcdefgh'
		if color == Color.BLACK:
			y = 8
		if self.name.lower() == 'queenside':
			s = s[::-1]
		for x in range(s.index('e'), len(s)):
			path.append(Square(s[x], y))
		return path