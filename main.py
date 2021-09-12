from piece import Piece
from color import Color
from square import Square
from pawn import Pawn
from rook import Rook
from bishop import Bishop
from knight import Knight
from queen import Queen
from king import King
from board import Board
from castling import Castling
import db
import pickle
import base64
from functools import reduce


def encode(obj):
    return base64.b64encode(pickle.dumps(obj)).decode()


def decode(s):
    return pickle.loads(s)


b = Board()
print(b)

# db.insert_row(encode(b), 1)
# print(db.select_all())
# db.update_row(black=2, status='in progress', id=4)
# db.delete_row(3)
print(db.select_all())

# while True:
# 	move = input()
# 	if move == '0-0':
# 		b.make_move(castling=Castling.KINGSIDE)
# 	elif move == '0-0-0':
# 		b.make_move(castling=Castling.QUEENSIDE)
# 	else:
# 		sq1 = Square(move[0], int(move[1]))
# 		sq2 = Square(move[3], int(move[4]))
# 		b.make_move(sq1=sq1, sq2=sq2)
# 	print(b)
# 	if b.is_checkmate(b.turn):
# 		print("Checkmate!")
# 		break
# 	if b.is_stalemate(b.turn):
# 		print("Checkmate!")
# 		break
# 	if b.is_check(b.turn):
# 		print("Check!")
