
class Piece:

	piece_dict = {
		'pawn': 1,
		'rook': 2,
		'knight': 3,
		'bishop': 4,
		'queen': 5,
		'king': 6
	}

	@classmethod
	def get_moves(cls, board, bx, by):
		return

	@classmethod
	def get_player(cls, piece):
		if 0 < piece < 7:
			return 1
		if 6 < piece < 13:
			return 2

	@classmethod
	def get_line_moves(cls, board, bx, by):
		moves = []
		dt = by
		db = 8 - by
		dl = bx
		dr = 8 - bx
		for i in range(dt):
			if board[by * 8 + bx - (8 * i)] == 0:
				moves.append(by * 8 + bx - (8 * i))
			else:
				if Piece.get_player(board[by * 8 + bx - (8 * i)]) != Piece.get_player(board[by * 8 + bx]):
					moves.append(by * 8 + bx - (8 * i))
				break
		for i in range(db):
			if board[by * 8 + bx + (8 * i)] == 0:
				moves.append(by * 8 + bx + (8 * i))
			else:
				if Piece.get_player(board[by * 8 + bx + (8 * i)]) != Piece.get_player(board[by * 8 + bx]):
					moves.append(by * 8 + bx + (8 * i))
				break
		for i in range(dl):
			if board[by * 8 + bx - i] == 0:
				moves.append(by * 8 + bx - i)
			else:
				if Piece.get_player(board[by * 8 + bx - i]) != Piece.get_player(board[by * 8 + bx]):
					moves.append(by * 8 + bx - i)
				break
		for i in range(dr):
			if board[by * 8 + bx + i] == 0:
				moves.append(by * 8 + bx + i)
			else:
				if Piece.get_player(board[by * 8 + bx + i]) != Piece.get_player(board[by * 8 + bx]):
					moves.append(by * 8 + bx + i)
				break
		return moves

	@classmethod
	def get_diagonal_moves(cls, board, bx, by):
		moves = []
		return NotImplemented
		return moves


piece = Piece('pawn', 0, 0, 0)
Piece.get_diagonal_moves([], piece)
