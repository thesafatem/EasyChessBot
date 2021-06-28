from square import Square
from color import Color
from pawn import Pawn
from knight import Knight
from bishop import Bishop 
from rook import Rook 
from queen import Queen 
from king import King

initial_board = {
	Square('a', 1): Rook(Color.WHITE, Square('a', 1)),
	Square('b', 1): Knight(Color.WHITE, Square('b', 1)),
	Square('c', 1): Bishop(Color.WHITE, Square('c', 1)),
	Square('d', 1): Queen(Color.WHITE, Square('d', 1)),
	Square('e', 1): King(Color.WHITE, Square('e', 1)),
	Square('f', 1): Bishop(Color.WHITE, Square('f', 1)),
	Square('g', 1): Knight(Color.WHITE, Square('g', 1)),
	Square('h', 1): Rook(Color.WHITE, Square('h', 1)),
	Square('a', 8): Rook(Color.BLACK, Square('a', 8)),
	Square('b', 8): Knight(Color.BLACK, Square('b', 8)),
	Square('c', 8): Bishop(Color.BLACK, Square('c', 8)),
	Square('d', 8): Queen(Color.BLACK, Square('d', 8)),
	Square('e', 8): King(Color.BLACK, Square('e', 8)),
	Square('f', 8): Bishop(Color.BLACK, Square('f', 8)),
	Square('g', 8): Knight(Color.BLACK, Square('g', 8)),
	Square('h', 8): Rook(Color.BLACK, Square('h', 8)),
	Square('a', 2): Pawn(Color.WHITE, Square('a', 2)),
	Square('b', 2): Pawn(Color.WHITE, Square('b', 2)),
	Square('c', 2): Pawn(Color.WHITE, Square('c', 2)),
	Square('d', 2): Pawn(Color.WHITE, Square('d', 2)),
	Square('e', 2): Pawn(Color.WHITE, Square('e', 2)),
	Square('f', 2): Pawn(Color.WHITE, Square('f', 2)),
	Square('g', 2): Pawn(Color.WHITE, Square('g', 2)),
	Square('h', 2): Pawn(Color.WHITE, Square('h', 2)),
	Square('a', 7): Pawn(Color.BLACK, Square('a', 7)),
	Square('b', 7): Pawn(Color.BLACK, Square('b', 7)),
	Square('c', 7): Pawn(Color.BLACK, Square('c', 7)),
	Square('d', 7): Pawn(Color.BLACK, Square('d', 7)),
	Square('e', 7): Pawn(Color.BLACK, Square('e', 7)),
	Square('f', 7): Pawn(Color.BLACK, Square('f', 7)),
	Square('g', 7): Pawn(Color.BLACK, Square('g', 7)),
	Square('h', 7): Pawn(Color.BLACK, Square('h', 7)),
}

reti_etude = {
	Square('h', 8): King(Color.WHITE, Square('h', 8)),
	Square('a', 6): King(Color.BLACK, Square('a', 6)),
	Square('c', 6): Pawn(Color.WHITE, Square('c', 6)),
	Square('h', 5): Pawn(Color.BLACK, Square('h', 5))
}