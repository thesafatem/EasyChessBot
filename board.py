from square import Square
from color import Color
from pawn import Pawn
from knight import Knight
from bishop import Bishop 
from rook import Rook 
from queen import Queen 
from king import King
from castling import Castling
from boards import initial_board, reti_etude
from PIL import Image, ImageDraw
import copy

class Board:
	def __init__(self):
		self.board = initial_board
		self.flipped = False
		self.turn = Color.WHITE
		self.en_passant = None

	def __str__(self):
		horizontal = [i for i in range(8, 0, -1)]
		vertical = "abcdefgh"
		if self.flipped:
			vertical = vertical[::-1]
			horizontal = horizontal[::-1]
		res = ""
		for y in horizontal:
			res += " " * 3 + '+---' * 8 + '+\n'
			res += f" {y} "
			for x in vertical:
				sq = Square(x, y)
				image = self.board.get(sq).img if self.board.get(sq) is not None else " "
				res += f"| {image} "
			res += "|\n"
		res += " " * 3 + '+---' * 8 + '+\n'
		res += " " * 3
		for x in vertical:
			res += f"  {x} "
		res += '\n'
		return res

	def get_coords(self, square, flipped):
		x = square.get_x()
		y = square.y
		if not flipped:
			y = 9 - y
		else:
			x = 9 - x
		return x, y

	def gen_board_image(self, flipped, small=False):
		board_image = Image.open('./media/board.png')
		for square, piece in self.board.items():
			x, y = self.get_coords(square, flipped)
			if piece is None:
				continue
			piece_image = Image.open(f'./media/{piece.image}')
			sz = piece_image.size
			board_image.paste(piece_image, ((x - 1) * sz[0], (y - 1) * sz[1]), piece_image)
		print(board_image.size)
		if small:
			board_image = board_image.resize((board_image.size[0] // 2, board_image.size[1] // 2))
		return board_image

	# add en-passant
	def is_achievable(self, sq1, sq2):
		piece = self.board.get(sq1)
		if piece is None:
			return False
		if not piece.can_move(sq2) and \
			((self.board.get(sq2) is None and (self.en_passant is None or self.en_passant != sq2)) \
				or (not piece.can_take(sq2))):
			return False
		path = piece.get_path(sq1, sq2)
		path.pop()
		for square in path:
			if self.board.get(square) is not None:
				return False
		return True

	def can_castling(self, castling):
		path = castling.get_path(self.turn)
		king = self.board.get(path[0])
		rook = self.board.get(path[-1])
		if not isinstance(king, King) or not king.is_first_move or \
			not isinstance(rook, Rook) or not rook.is_first_move:
			# print('yyy')
			return False
		for i in range(1, len(path) - 1):
			sq = path[i]
			if self.board.get(sq) is not None:
				# print('xxx')
				return False
		for i in range(3):
			for x in "abcdefgh":
				for y in range(1, 9):
					piece = self.board.get(Square(x, y))
					if piece is None or piece.color == self.turn:
						continue
					if self.is_achievable(Square(x, y), path[i]):
						print(piece, path[i])
						return False
		return True

	def can_move(self, sq1, sq2):
		if not self.is_achievable(sq1, sq2):
			return False
		piece = self.board.get(sq1)
		if self.board.get(sq2) is not None:
			# print(piece.color, self.board.get(sq2).color)
			if piece.color == self.board.get(sq2).color:
				return False
			if not piece.can_take(sq2): # pawn can't take straight
				return False
		new_board = copy.deepcopy(self)
		new_board.make_move_forcibly(sq1, sq2)
		if new_board.is_check(piece.color):
			return False
		return True

	def get_king(self, color):
		for x in "abcdefgh":
			for y in range(1, 9):
				sq = Square(x, y)
				piece = self.board.get(sq)
				if piece is not None and piece.__class__.__name__ == 'King' and piece.color == color:
					return sq

	def is_check(self, color):
		king_sq = self.get_king(color)
		for x in "abcdefgh":
			for y in range(1, 9):
				sq = Square(x, y)
				piece = self.board.get(sq)
				if piece is not None and piece.color != color and self.is_achievable(sq, king_sq):
					return True

	def make_move_forcibly(self, sq1, sq2):
		piece = self.board.get(sq1)
		piece.square = sq2
		piece.is_first_move = False
		self.board[sq1] = None
		self.board[sq2] = piece
		self.turn = Color.inv(self.turn)

	def make_move(self, **kwargs):
		castling = kwargs.get('castling')
		if castling is not None:
			if not self.can_castling(castling):
				return False
			else:
				path = castling.get_path(self.turn)
				king = self.board.get(path[0])
				rook = self.board.get(path[-1])
				king.square = path[2]
				rook.square = path[1]
				king.is_first_move = False
				rook.is_first_move = False
				self.board[path[0]] = None
				self.board[path[-1]] = None
				self.board[path[1]] = rook
				self.board[path[2]] = king
				self.turn = Color.inv(self.turn)
				self.flipped = not self.flipped
				return True
		else:
			sq1 = kwargs.get('sq1')
			sq2 = kwargs.get('sq2')
			piece = self.board.get(sq1)
			if self.can_move(sq1, sq2) and piece.color == self.turn:
				if isinstance(piece, Pawn) and piece.can_double_move(sq2):
					sq = Square(sq1.x, (sq1.y + sq2.y) // 2)
					self.en_passant = sq
				else:
					self.en_passant = None
				self.make_move_forcibly(sq1, sq2)
				if isinstance(piece, Pawn) and (sq2.y == 8 or sq2.y == 1):
					promoted_piece = Pawn.ask_promotion(piece.color, sq2)
					self.board[sq2] = promoted_piece
				self.flipped = not self.flipped
				return True
			return False

	def has_moves(self, color):
		for from_x in "abcdefgh":
			for from_y in range(1, 9):
				from_sq = Square(from_x, from_y)
				piece = self.board.get(from_sq)
				if piece is None or piece.color != color:
					continue
				for to_x in "abcdefgh":
					for to_y in range(1, 9):
						to_sq = Square(to_x, to_y)
						if self.can_move(from_sq, to_sq):
							return True
		return False

	def is_checkmate(self, color):
		return self.is_check(color) and not self.has_moves(color)

	def is_stalemate(self, color):
		return not self.is_check(color) and not self.has_moves(color)