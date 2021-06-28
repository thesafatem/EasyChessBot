from enum import Enum

class Color(Enum):
	WHITE = 0
	BLACK = 1

	def __str__(self):
		return self.name.lower()

	@staticmethod
	def inv(color):
		if color == Color.WHITE:
			return Color.BLACK
		else:
			return Color.WHITE