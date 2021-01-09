from math import sin, cos, pi
from copy import deepcopy

# TODO:
#   check for checkmate
#   stalement

class CheckException(Exception):
	pass

class IlegalMoveException(Exception):
	pass

class InvalidNotationException(Exception):
	pass

WHITE = True
BLACK = False

class Game:

	def __init__(self):
		'''
		self.board = [
			['br', 'bn', 'bb', 'bq', 'bk', 'bb', 'bn', 'br'],
			['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
			[None, None, None, None, None, None, None, None],
			[None, None, None, None, None, None, None, None],
			[None, None, None, None, None, None, None, None],
			[None, None, None, None, None, None, None, None],
			['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
			['wr', 'wn', 'wb', 'wq', 'wk', 'wb', 'wn', 'wr']
		]
		'''

		self.board = [
			['br', None, None, None, 'bk', None, None, None],
			['bp', 'bp', 'bp', None, 'bp', 'bp', 'bp', 'bp'],
			[None, None, None, None, None, None, None, None],
			[None, None, None, None, None, None, None, 'bb'],
			[None, None, None, None, None, None, None, None],
			[None, None, None, None, None, None, None, None],
			['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
			[None, None, 'wb', None, 'wk', None, 'br', None]
		]

		self.moves = []

		self.turn = WHITE

		self.en_passant_coord_white = None
		self.en_passant_coord_black = None

		self.en_passant_flag_white = False
		self.en_passant_flag_black = False

		self.en_passant_just_now = False

		self.white_king_has_moved = False
		self.black_king_has_moved = False

		self.white_king_rook_has_moved = False
		self.white_queen_rook_has_moved = False

		self.black_king_rook_has_moved = False
		self.black_queen_rook_has_moved = False

	# -----------------------------------------------------------------------------------------------------------------
	#                                              AUXILIARY FUNCTIONS
	# -----------------------------------------------------------------------------------------------------------------

	def get_board(self):
		return self.board

	def get_piece_color(self, piece):
		if piece[0] == 'w':
			return WHITE
		elif piece[0] == 'b':
			return BLACK
		else:
			raise Exception("It's not possible to identify the piece's color")

	def get_column(self, char):
		return ord(char) - 97

	def get_row(self, digit):
		return abs(int(digit) - 8)

	def print_board(self):
		for row in self.board:
			print(row)

	def is_piece_white(self, piece):
		return piece[0] == 'w'

	def is_piece_black(self, piece):
		return piece[0] == 'b'

	def is_normal_movement(self, movement, add):
		return movement[1 + add].isalpha() and movement[2 + add].isdigit()

	def is_same_row_movement(self, movement, add):
		return movement[1].isalpha() and movement[2 + add].isalpha()

	def is_same_col_movement(self, movement, add):
		return movement[1].isdigit() and movement[2 + add].isalpha()

	def is_move_capture(self, move):
		return 'x' in move

	def get_king_coord(self, color):
		king_str = None
		if color == WHITE:
			king_str = 'wk'
		else:
			king_str = 'bk'

		for i in range(8):
			for j in range(8):
				cell = self.board[i][j]
				if cell is not None and cell == king_str:
					return (i, j)

		raise Exception('King not found')

	# -----------------------------------------------------------------------------------------------------------------
	#                                                 FINDERS
	# -----------------------------------------------------------------------------------------------------------------
	# These following functions are designed find the coordinates of the piece to be moved if it's not explicit in the
	# algebraic notation. In this case, it's quickly translated in the handlers.
	# -----------------------------------------------------------------------------------------------------------------

	def find_pawn(self, color, column, limit):
		piece_coord = None
		if color == WHITE:
			for i in range(6, limit, -1):
				piece = self.board[i][column]
				if piece is not None and self.is_piece_white(piece):
					piece_coord = (i, column)
		# it's necessary not to break here because there may be double pawns in a column
		else:
			for i in range(1, limit):
				piece = self.board[i][column]
				if piece is not None and self.is_piece_black(piece):
					piece_coord = (i, column)
		# it's necessary not to break here because there may be double pawns in a column

		return piece_coord

	def find_capturer_pawn(self, color, destination_row, origin_column):
		if color == WHITE:
			return (destination_row + 1, origin_column)
		else:
			return (destination_row - 1, origin_column)

	def find_rook(self, color, destination):
		found = False
		rook_coords = []

		# going throw columns
		for col in range(8):
			piece = self.board[destination[0]][col]
			if piece is not None and piece[1] == 'r' and self.get_piece_color(piece) == color:
				found = True
				rook_coords.append((destination[0], col))

		# going throw rows
		for row in range(8):
			piece = self.board[row][destination[1]]
			if piece is not None and piece[1] == 'r' and self.get_piece_color(piece) == color:
				found = True
				rook_coords.append((row, destination[1]))

		if found:
			return rook_coords
		else:
			raise Exception('Rook not found. Check for bugs')

	def find_knight(self, color, destination):
		found = False
		coords = []
		i = 0
		while i < 2 * pi:
			row = destination[0] + 2 * int(cos(i)) + int(sin(i))
			col = destination[1] + 2 * int(sin(i)) + int(cos(i))
			if self.validate_coord_out_of_board((row, col)):
				piece = self.board[row][col]
				if piece is not None and piece[1] == 'n' and self.get_piece_color(piece) == color:
					found = True
					coords.append((row, col))

			row = destination[0] + 2 * int(cos(i)) - int(sin(i))
			col = destination[1] + 2 * int(sin(i)) - int(cos(i))
			if self.validate_coord_out_of_board((row, col)):
				piece = self.board[row][col]
				if piece is not None and piece[1] == 'n' and self.get_piece_color(piece) == color:
					found = True
					coords.append((row, col))

			i += pi / 2

		if found:
			return coords
		else:
			raise IlegalMoveException('No knight was found')

	def find_bishop(self, color, destination):
		for i in range(-1, 2, 2):
			for j in range(-1, 2, 2):
				coord = list(destination)
				coord[0] += i
				coord[1] += j
				while self.validate_coord_out_of_board(coord):
					piece = self.board[coord[0]][coord[1]]
					if piece is not None and piece[1] == 'b' and self.get_piece_color(piece) == color:
						return (coord[0], coord[1])
					coord[0] += i
					coord[1] += j

		raise IlegalMoveException('Could not find bishop')

	def find_queen(self, color, destination):
		# rook-like part
		# going throw columns
		for col in range(8):
			piece = self.board[destination[0]][col]
			if piece is not None and piece[1] == 'q' and self.get_piece_color(piece) == color:
				return (destination[0], col)

		# going throw rows
		for row in range(8):
			piece = self.board[row][destination[1]]
			if piece is not None and piece[1] == 'q' and self.get_piece_color(piece) == color:
				return (row, destination[1])

		# bishop-like part
		for i in range(-1, 2, 2):
			for j in range(-1, 2, 2):
				coord = list(destination)
				coord[0] += i
				coord[1] += j
				while self.validate_coord_out_of_board(coord):
					piece = self.board[coord[0]][coord[1]]
					if piece is not None and piece[1] == 'q' and self.get_piece_color(piece) == color:
						return (coord[0], coord[1])
					coord[0] += i
					coord[1] += j

		raise IlegalMoveException('Queen not found')

	def find_king(self, color, destination):
		for i in range(-1, 2):
			for j in range(-1, 2):
				if (i != 0 or j != 0) and self.validate_coord_out_of_board((destination[0] + i, destination[1] + j)):
					piece = self.board[destination[0] + i][destination[1] + j]
					if piece is not None and piece[1] == 'k' and self.get_piece_color(piece) == color:
						return (destination[0] + i, destination[1] + j)

		raise IlegalMoveException('Could not find the king')

	# -----------------------------------------------------------------------------------------------------------------
	#                                               VALIDATORS
	# -----------------------------------------------------------------------------------------------------------------
	# Once the piece to be moved is found, these functions validate if the move is legal. If not, it's exceptions are
	# raised describing which rule was broken.
	#
	# TODO: check out if these functions still work with more than the default amount of pieces, because of pawn
	# upgrades
	# -----------------------------------------------------------------------------------------------------------------

	def validate_coord_out_of_board(self, coord):
		return 0 <= coord[0] <= 7 and 0 <= coord[1] <= 7

	def validate_pawn_move(self, piece_coord, destination):
		# destination and piece_coord: (row, column)
		piece = self.board[piece_coord[0]][piece_coord[1]]

		if piece is None:
			raise IlegalMoveException('There is no piece in the origin square')

		if piece[1] != 'p':
			raise IlegalMoveException('Wrong piece passed as parameter:', piece)

		# check if same row
		if piece_coord[1] == destination[1]:

			# check if column distance is ok
			if abs(piece_coord[1] - destination[1]) != 0:
				raise IlegalMoveException('Column distance is invalid')

			# check if there is any piece in the destination
			destination_piece = self.board[destination[0]][destination[1]]
			if destination_piece is not None:
				raise IlegalMoveException('There is a piece in the destination square')

			row_distance = piece_coord[0] - destination[0]

			if piece[0] == 'w':
				# check if distance is correct
				if row_distance == 2:
					if piece_coord[0] != 6:
						raise IlegalMoveException('Wrong row distance:', row_distance)
					elif self.board[piece_coord[0] - 1][piece_coord[1]] is not None:
						raise IlegalMoveException('There is another piece in the way')

					self.en_passant_coord_white = (5, piece_coord[1])
					self.en_passant_just_now = True
				elif row_distance != 1:
					raise IlegalMoveException('Wrong row distance', row_distance)
			elif piece[0] == 'b':
				# check if distance is correct
				if row_distance == -2:
					if piece_coord[0] != 1:
						raise IlegalMoveException('Wrong row distance:', row_distance)
					elif self.board[piece_coord[0] + 1][piece_coord[1]] is not None:
						raise IlegalMoveException('There is another piece in the way')

					self.en_passant_coord_black = (2, piece_coord[1])
					self.en_passant_just_now = True
				elif row_distance != -1:
					raise IlegalMoveException('Wrong row distance', row_distance)

		else:

			raise IlegalMoveException('This is not a capture move')

	def validate_capture_with_pawn(self, piece_coord, destination):
		# destination and piece_coord: [row, column]
		piece = self.board[piece_coord[0]][piece_coord[1]]

		if not self.validate_coord_out_of_board(destination):
			raise InvalidNotationException('Destination out of boundries')

		if piece is None:
			raise IlegalMoveException('There is no piece in the origin square')

		if piece[1] != 'p':
			raise IlegalMoveException('Wrong piece passed as parameter:', piece)

		# check if different row
		if piece_coord[1] != destination[1]:
			# check if column distance is ok
			if abs(piece_coord[1] - destination[1]) != 1:
				raise IlegalMoveException('Column distance is invalid')

			# check if there is enemy piece in the destination
			destination_piece = self.board[destination[0]][destination[1]]
			if destination_piece is None:
				# en passant possibility
				if (self.is_piece_white(piece) and self.en_passant_coord_black != destination) or (
						self.is_piece_black(piece) and self.en_passant_coord_white != destination):
					raise IlegalMoveException('There is no piece in the destination square to capture')
				else:
					# set a flag to sign on move_piece function that a en passant was done
					if self.is_piece_white(piece):
						self.en_passant_flag_white = True
					else:
						self.en_passant_flag_black = True
			elif self.get_piece_color(destination_piece) == self.get_piece_color(piece):
				raise IlegalMoveException("You can't capture your own piece")

			if piece[0] == 'w':
				# check if distance is correct
				if piece_coord[0] - destination[0] != 1:
					raise IlegalMoveException('Wrong row distance')
			elif piece[0] == 'b':
				# check if distance is correct
				if piece_coord[0] - destination[0] != -1:
					raise IlegalMoveException('Wrong row distance')
			else:
				raise IlegalMoveException('Wrong color passed as parameter:', piece)
		else:
			raise IlegalMoveException('This is not a capture move')

	def validate_rook_move(self, piece_coord, destination, capture):
		# destination and piece_coord: (row, column)
		piece = self.board[piece_coord[0]][piece_coord[1]]

		if piece is None:
			raise IlegalMoveException('There is no piece in the origin square')

		if piece[1] != 'r':
			raise IlegalMoveException('Wrong piece passed as parameter:', piece)

		if piece_coord[0] != destination[0] and piece_coord[1] != destination[1]:
			raise IlegalMoveException('Piece not in the same row or column as destination')

		if piece_coord[0] == destination[0] and piece_coord[1] == destination[1]:
			raise IlegalMoveException("You can't move to the same square")

		if piece_coord[0] == destination[0]:
			# same row as destination
			row = piece_coord[0]

			if piece_coord[1] < destination[1]:
				start = piece_coord[1]
				end = destination[1]
			else:
				start = destination[1]
				end = piece_coord[1]

			for i in range(start + 1, end):
				if self.board[row][i] is not None:
					raise IlegalMoveException('There are other pieces between the origin and destination')
		else:
			# same column as destination
			col = piece_coord[1]

			if piece_coord[0] < destination[0]:
				start = piece_coord[0]
				end = destination[0]
			else:
				start = destination[0]
				end = piece_coord[0]

			for i in range(start + 1, end):
				if self.board[i][col] is not None:
					raise IlegalMoveException('There are other pieces between the origin and destination')

		destination_piece = self.board[destination[0]][destination[1]]
		if capture:
			if destination_piece is None:
				raise IlegalMoveException('There is no piece in the square to be captured')
			if self.get_piece_color(destination_piece) == self.get_piece_color(piece):
				raise IlegalMoveException("You can't capture your own piece")
		if not capture and destination_piece is not None:
			raise IlegalMoveException("That is a place where you're trying to move. Try the capture move")

	def validate_knight_move(self, piece_coord, destination, capture):
		# destination and piece_coord: (row, column)
		piece = self.board[piece_coord[0]][piece_coord[1]]

		if piece is None:
			raise IlegalMoveException('There is no piece in the origin square')

		if piece[1] != 'n':
			raise IlegalMoveException('Wrong piece passed as parameter:', piece)

		destination_piece = self.board[destination[0]][destination[1]]
		if capture:
			if destination_piece is None:
				raise IlegalMoveException('There is no piece in the square to be captured')
			if self.get_piece_color(destination_piece) == self.get_piece_color(piece):
				raise IlegalMoveException("You can't capture your own piece")
		if not capture and destination_piece is not None:
			raise IlegalMoveException("That is a place where you're trying to move. Try the capture move")

	def validate_bishop_move(self, piece_coord, destination, capture):
		# destination and piece_coord: (row, column)
		piece = self.board[piece_coord[0]][piece_coord[1]]

		if piece is None:
			raise IlegalMoveException('There is no piece in the origin square')

		if piece[1] != 'b':
			raise IlegalMoveException('Wrong piece passed as parameter:', piece)

		# get the direction to go to
		row_incr = None
		if destination[0] - piece_coord[0] > 0:
			row_incr = 1
		elif destination[0] - piece_coord[0] < 0:
			row_incr = -1
		else:
			raise IlegalMoveException("Can't realize this move because both pieces are in the same row")

		col_incr = None
		if destination[1] - piece_coord[1] > 0:
			col_incr = 1
		elif destination[1] - piece_coord[1] < 0:
			col_incr = -1
		else:
			raise IlegalMoveException("Can't realize this move because both pieces are in the same column")

		# check if the path to the destination is empty
		coord = list(piece_coord)
		coord[0] += row_incr
		coord[1] += col_incr
		while tuple(coord) != destination:
			square = self.board[coord[0]][coord[1]]
			if square is not None:
				raise IlegalMoveException('There is at least one piece in the path between the two pieces:', coord)

			coord[0] += row_incr
			coord[1] += col_incr

		destination_piece = self.board[destination[0]][destination[1]]
		if capture:
			if destination_piece is None:
				raise IlegalMoveException('There is no piece in the square to be captured')
			if self.get_piece_color(destination_piece) == self.get_piece_color(piece):
				raise IlegalMoveException("You can't capture your own piece")
		if not capture and destination_piece is not None:
			raise IlegalMoveException("That is a place where you're trying to move. Try the capture move")

	def validate_queen_move(self, piece_coord, destination, capture):
		# destination and piece_coord: (row, column)
		piece = self.board[piece_coord[0]][piece_coord[1]]

		if piece is None:
			raise IlegalMoveException('There is no piece in the origin square')

		if piece[1] != 'q':
			raise IlegalMoveException('Wrong piece passed as parameter:', piece)

		if piece_coord[0] == destination[0] and piece_coord[1] == destination[1]:
			raise IlegalMoveException("You can't move to the same square")

		if abs(piece_coord[0] - destination[0]) == abs(piece_coord[1] - destination[1]):
			# behaving like a bishop
			# get the direction to go to
			row_incr = None
			if destination[0] - piece_coord[0] > 0:
				row_incr = 1
			elif destination[0] - piece_coord[0] < 0:
				row_incr = -1
			else:
				raise IlegalMoveException("Can't realize this move because both pieces are in the same row")

			col_incr = None
			if destination[1] - piece_coord[1] > 0:
				col_incr = 1
			elif destination[1] - piece_coord[1] < 0:
				col_incr = -1
			else:
				raise IlegalMoveException("Can't realize this move because both pieces are in the same column")

			# check if the path to the destination is empty
			coord = list(piece_coord)
			coord[0] += row_incr
			coord[1] += col_incr
			while tuple(coord) != destination:
				square = self.board[coord[0]][coord[1]]
				if square is not None:
					raise IlegalMoveException('There is at least one piece in the path between the two pieces:', coord)

				coord[0] += row_incr
				coord[1] += col_incr
		elif piece_coord[0] == destination[0] or piece_coord[1] == destination[1]:
			# behaving like a rook
			if piece_coord[0] == destination[0]:
				# same row as destination
				row = piece_coord[0]

				if piece_coord[1] < destination[1]:
					start = piece_coord[1]
					end = destination[1]
				else:
					start = destination[1]
					end = piece_coord[1]

				for i in range(start + 1, end):
					if self.board[row][i] is not None:
						raise IlegalMoveException('There are other pieces between the origin and destination')
			else:
				# same column as destination
				col = piece_coord[1]

				if piece_coord[0] < destination[0]:
					start = piece_coord[0]
					end = destination[0]
				else:
					start = destination[0]
					end = piece_coord[0]

				for i in range(start + 1, end):
					if self.board[i][col] is not None:
						raise IlegalMoveException('There are other pieces between the origin and destination')

		destination_piece = self.board[destination[0]][destination[1]]
		if capture:
			if destination_piece is None:
				raise IlegalMoveException('There is no piece in the square to be captured')
			if self.get_piece_color(destination_piece) == self.get_piece_color(piece):
				raise IlegalMoveException("You can't capture your own piece")
		if not capture and destination_piece is not None:
			raise IlegalMoveException("That is a place where you're trying to move. Try the capture move")

	def validate_king_move(self, piece_coord, destination, capture):
		# there is no need to check if there is something in between the two pieces because the king can only move one
		# square each time
		piece = self.board[piece_coord[0]][piece_coord[1]]
		destination_square = self.board[destination[0]][destination[1]]

		if capture:
			if destination_square is None:
				raise IlegalMoveException('There is nothing to capture in this square')
			elif self.get_piece_color(piece) == self.get_piece_color(destination_square):
				raise IlegalMoveException("You cant' capture your own piece")
		else:
			if destination_square is not None:
				raise IlegalMoveException('There is a piece in the square you want to move to')

		if abs(piece_coord[0] - destination[0]) > 1 or abs(piece_coord[1] - destination[1]) > 1:
			raise IlegalMoveException('The destination is too far away from the king')

	def validate_castle_move(self, movement):
		if self.turn == WHITE:
			row = 7
		else:
			row = 0

		if (self.turn == WHITE and self.white_king_has_moved) or (self.turn == BLACK and self.black_king_rook_has_moved):
			raise IlegalMoveException('The king has already moved')

		try:
			# we already know that the queen is in the default square because of previous validations
			self.validate_square_in_check((row, 4), piece_at_square=True)
		except CheckException:
			raise IlegalMoveException('The king is in check')

		if movement == '0-0' or movement == 'O-O':
			# king side
			if self.board[row][7] is None:
				raise IlegalMoveException('There is no rook to castle with')

			if (self.turn == WHITE and self.white_king_rook_has_moved) or (self.turn == BLACK and self.black_king_rook_has_moved):
				raise IlegalMoveException('The rook has already moved')

			for i in range(5, 7):
				if self.board[row][i] is not None:
					raise IlegalMoveException('There is at least one piece in between the king and the rook')

				try:
					self.validate_square_in_check((row, i), piece_at_square=False)
				except CheckException:
					raise IlegalMoveException('There are squares in check in the way')

		elif movement == '0-0-0' or movement == 'O-O-O':
			# queen side
			if self.board[row][0] is None:
				raise IlegalMoveException('There is no rook to castle with')

			if (self.turn == WHITE and self.white_queen_rook_has_moved) or (self.turn == BLACK and self.black_queen_rook_has_moved):
				raise IlegalMoveException('The rook has already moved')

			for i in range(1, 4):
				if self.board[row][i] is not None:
					raise IlegalMoveException('There is at least one piece in between the king and the rook')

				try:
					self.validate_square_in_check((row, i), piece_at_square=False)
				except CheckException:
					raise IlegalMoveException('There are squares in check in the way:', (row, i))

		else:
			raise IlegalMoveException('This move is invalid')

	# -----------------------------------------------------------------------------------------------------------------
	#                                      CHECK AND ENDGAME VALIDATORS
	# -----------------------------------------------------------------------------------------------------------------
	#
	# -----------------------------------------------------------------------------------------------------------------

	def validate_move_causes_self_check(self, piece_coord, destination):
		board_copy = deepcopy(self.board)

		king_str = None

		if self.turn == WHITE:
			king_str = 'wk'
		else:
			king_str = 'bk'

		# alterations on the board
		self.board[destination[0]][destination[1]] = self.board[piece_coord[0]][piece_coord[1]]
		self.board[piece_coord[0]][piece_coord[1]] = None

		try:
			self.validate_square_in_check(self.get_king_coord(self.turn), piece_at_square=True)
		except CheckException as ce:
			raise CheckException('This move causes yourself a check')
		finally:
			# going back to normal
			self.board = deepcopy(board_copy)

	def validate_square_in_check(self, piece_coord, piece_at_square):
		# the not piece_at_square is a fix because in the castle calculation, it would not consider the path between the rook
		# and king as in check becuase there was no piece in those squares

		# rook part
		try:
			e_rook_coords = self.find_rook(not self.turn, piece_coord)
			for c in e_rook_coords:
				self.validate_rook_move(c, piece_coord, piece_at_square)

			raise CheckException()
		except CheckException:
			raise CheckException()
		except:
			# Couldn't capture
			None

		# knight part
		try:
			e_knight_coords = self.find_knight(not self.turn, piece_coord)
			for c in e_knight_coords:
				self.validate_knight_move(c, piece_coord, piece_at_square)

			raise CheckException()
		except CheckException:
			raise CheckException()
		except:
			# Couldn't capture
			pass

		# bishop part
		try:
			e_bishop_coord = self.find_bishop(not self.turn, piece_coord)
			self.validate_bishop_move(e_bishop_coord, piece_coord, piece_at_square)
			raise CheckException()
		except CheckException:
			raise CheckException()
		except:
			# Couldn't capture
			pass

		# queen part
		try:
			e_queen_coord = self.find_queen(not self.turn, piece_coord)
			self.validate_queen_move(e_queen_coord, piece_coord, piece_at_square)
			raise CheckException()
		except CheckException:
			raise CheckException()
		except:
			# Couldn't capture
			None

		# king part
		try:
			e_king_coord = None

			if self.turn == WHITE:
				e_king_coord = self.get_king_coord(BLACK)
			else:
				e_king_coord = self.get_king_coord(WHITE)

			self.validate_king_move(e_king_coord, piece_coord, piece_at_square)
			raise CheckException()
		except CheckException:
			raise CheckException()
		except:
			# Couldn't capture
			None

		# it's needed to validate the pawns manually here because the other functions don't work in this case
		try:
			if self.turn == WHITE:
				king_col = piece_coord[1]
				if king_col - 1 >= 0:
					possible_pawn = self.board[piece_coord[0] - 1][king_col - 1]
					if possible_pawn is not None and possible_pawn == 'bp':
						raise CheckException()
				if king_col + 1 <= 8:
					possible_pawn = self.board[piece_coord[0] - 1][king_col + 1]
					if possible_pawn is not None and possible_pawn == 'bp':
						raise CheckException()
			else:
				king_col = piece_coord[1]
				if king_col - 1 >= 0:
					possible_pawn = self.board[piece_coord[0] + 1][king_col - 1]
					if possible_pawn is not None and possible_pawn == 'wp':
						raise CheckException()
				if king_col + 1 <= 8:
					possible_pawn = self.board[piece_coord[0] + 1][king_col + 1]
					if possible_pawn is not None and possible_pawn == 'wp':
						raise CheckException()
		except CheckException:
			raise CheckException()
		except:
			# Couldn't capture
			pass

	def is_checkmate(self):
		king_coord = self.get_king_coord(self.turn)
		color_char = None
		if self.turn == WHITE:
			color_char = 'w'
		else:
			color_char = 'b'

		try:
			self.validate_square_in_check(king_coord, piece_at_square=True)
			return False
		except CheckException:
			pass

		for i in range(8):
			for j in range(8):
				cell = self.board[i][j]
				if cell is not None and cell[0] == color_char:
					if cell[1] == 'p':
						if self.pawn_move_stops_check(i, j):
							return False
					elif cell[1] == 'r':
						if self.rook_move_stops_check(i, j):
							return False
					elif cell[1] == 'n':
						if self.knight_move_stops_check(i, j):
							return False
					elif cell[1] == 'b':
						if self.bishop_move_stops_check(i, j):
							return False
					elif cell[1] == 'q':
						if self.queen_move_stops_check(i, j):
							return False
					elif cell[1] == 'k':
						if self.king_move_stops_check(i, j):
							return False

		return True

	def rook_move_stops_check(self, i, j):
		# going throw the rows
		for row in range(i + 1, 8):
			try:
				self.validate_rook_move((i, j), (row, j), self.board[row][j] is not None)
				self.validate_move_causes_self_check((i, j), (row, j))
				return True
			except IlegalMoveException:
				break
			except CheckException:
				pass

		for row in range(i - 1, -1, -1):
			try:
				self.validate_rook_move((i, j), (row, j), self.board[row][j] is not None)
				self.validate_move_causes_self_check((i, j), (row, j))
				return True
			except IlegalMoveException:
				break
			except CheckException:
				pass

		# going throw the columns
		for col in range(j + 1, 8):
			try:
				self.validate_rook_move((i, j), (i, col), self.board[i][col] is not None)
				self.validate_move_causes_self_check((i, j), (i, col))
				return True
			except IlegalMoveException:
				break
			except CheckException:
				pass

		for col in range(j - 1, -1, -1):
			try:
				self.validate_rook_move((i, j), (i, col), self.board[i][col] is not None)
				self.validate_move_causes_self_check((i, j), (i, col))
				return True
			except IlegalMoveException:
				break
			except CheckException:
				pass

		return False

	def knight_move_stops_check(self, i, j):
		ang = 0
		while ang < 2 * pi:
			row = i + 2 * int(cos(ang)) + int(sin(ang))
			col = j + 2 * int(sin(ang)) + int(cos(ang))
			if self.validate_coord_out_of_board((row, col)):
				try:
					self.validate_knight_move((i, j), (row, col), self.board[row][col] is not None)
					self.validate_move_causes_self_check((i, j), (row, col))
					return True
				except CheckException:
					pass
				except IlegalMoveException:
					pass

			row = i + 2 * int(cos(ang)) - int(sin(ang))
			col = j + 2 * int(sin(ang)) - int(cos(ang))
			if self.validate_coord_out_of_board((row, col)):
				try:
					self.validate_knight_move((i, j), (row, col), self.board[row][col] is not None)
					self.validate_move_causes_self_check((i, j), (row, col))
					return True
				except CheckException:
					pass
				except IlegalMoveException:
					pass

			ang += pi / 2

	def bishop_move_stops_check(self, i, j):
		for y in range(-1, 2, 2):
			for x in range(-1, 2, 2):
				pos = [i + y, j + x]
				while self.validate_coord_out_of_board(pos):
					try:
						self.validate_bishop_move((i, j), tuple(pos), self.board[pos[0]][pos[1]] is not None)
						self.validate_move_causes_self_check((i, j), tuple(pos))
						return True
					except IlegalMoveException:
						break
					except CheckException:
						pass

					pos[0] += y
					pos[1] += x

		return False

	def queen_move_stops_check(self, i, j):
		# rook part
		# going throw the rows
		for row in range(i + 1, 8):
			try:
				self.validate_queen_move((i, j), (row, j), self.board[row][j] is not None)
				self.validate_move_causes_self_check((i, j), (row, j))
				return True
			except IlegalMoveException:
				break
			except CheckException:
				pass

		for row in range(i - 1, -1, -1):
			try:
				self.validate_queen_move((i, j), (row, j), self.board[row][j] is not None)
				self.validate_move_causes_self_check((i, j), (row, j))
				return True
			except IlegalMoveException:
				break
			except CheckException:
				pass

		# going throw the columns
		for col in range(j + 1, 8):
			try:
				self.validate_queen_move((i, j), (i, col), self.board[i][col] is not None)
				self.validate_move_causes_self_check((i, j), (i, col))
				return True
			except IlegalMoveException:
				break
			except CheckException:
				pass

		for col in range(j - 1, -1, -1):
			try:
				self.validate_queen_move((i, j), (i, col), self.board[i][col] is not None)
				self.validate_move_causes_self_check((i, j), (i, col))
				return True
			except IlegalMoveException:
				break
			except CheckException:
				pass

		# bishop part
		for y in range(-1, 2, 2):
			for x in range(-1, 2, 2):
				pos = [i + y, j + x]
				while self.validate_coord_out_of_board(pos):
					self.validate_queen_move((i, j), tuple(pos), self.board[pos[0]][pos[1]] is not None)
					try:
						self.validate_queen_move((i, j), tuple(pos), self.board[pos[0]][pos[1]] is not None)
						self.validate_move_causes_self_check((i, j), tuple(pos))
						return True
					except IlegalMoveException as e:
						print(e)
						break
					except CheckException:
						pass

					pos[0] += y
					pos[1] += x

		return False

	def king_move_stops_check(self, i, j):
		for y in range(-1, 2):
			for x in range(-1, 2):
				des = (i + y, j + x)
				if (y != 0 or x != 0) and self.validate_coord_out_of_board(des):
					try:
						self.validate_king_move((i, j), des, self.board[des[0]][des[1]] is not None)
						self.validate_move_causes_self_check((i, j), des)
						return True
					except IlegalMoveException:
						break
					except CheckException:
						pass

		return False

	def pawn_move_stops_check(self, i, j):
		spawn_row = None
		direction = None
		if self.turn == WHITE:
			spawn_row = 6
			direction = -1
		else:
			spawn_row = 1
			direction = 1

		# check for one step moves
		try:
			destination = (i+direction, j)
			self.validate_pawn_move((i, j), destination)
			self.validate_move_causes_self_check((i, j), destination)
			return True
		except CheckException:
			pass
		except IlegalMoveException:
			pass

		# check for two step moves
		try:
			destination = (i + (2 * direction), j)
			self.validate_pawn_move((i, j), destination)
			self.validate_move_causes_self_check((i, j), destination)
			return True
		except CheckException:
			pass
		except IlegalMoveException:
			pass

		try:
			destination = (i + direction, j - 1)
			self.validate_capture_with_pawn((i, j), destination)
			self.validate_move_causes_self_check((i, j), destination)
			return True
		except CheckException:
			pass
		except IlegalMoveException:
			pass
		except InvalidNotationException:
			pass

		try:
			destination = (i + direction, j + 1)
			self.validate_capture_with_pawn((i, j), destination)
			self.validate_move_causes_self_check((i, j), destination)
			return True
		except CheckException:
			pass
		except IlegalMoveException:
			pass
		except InvalidNotationException:
			pass

		return False

	# -----------------------------------------------------------------------------------------------------------------
	#                                ALGEBRAIC NOTATION TRANSLATORS AND MOVE HANDLERS
	# -----------------------------------------------------------------------------------------------------------------
	# These functions are designed to translate the algebraic notation into data to be used on the other functions.
	# -----------------------------------------------------------------------------------------------------------------

	def move_piece(self, movement):
		destination = None
		piece_coord = None

		if movement[0].isupper():
			# if the movement is of capture, it's just easier if we shift the reading one character to the right
			add = 0
			if self.is_move_capture(movement):
				add = 1

			if movement[0] == 'R':
				# rook
				destination, piece_coord = self.handle_rook_move(movement, add)
			elif movement[0] == 'N':
				# knight
				destination, piece_coord = self.handle_knight_move(movement, add)
			elif movement[0] == 'B':
				# bishop
				destination, piece_coord = self.handle_bishop_move(movement, add)
			elif movement[0] == 'Q':
				# queen
				destination, piece_coord = self.handle_queen_move(movement, add)
			elif movement[0] == 'K':
				# king
				destination, piece_coord = self.handle_king_move(movement, add)
			else:
				raise InvalidNotationException('This command is invalid')
		elif movement[0] == 'x' or 97 <= ord(movement[0]) <= 104:
			# pawn
			destination, piece_coord = self.handle_pawn_move(movement)
		elif movement[0] == '0':
			# castle
			self.handle_castle(movement)
		else:
			raise InvalidNotationException('This command is invalid')

		'''
		print('move:', movement)
		print('dest:', destination)
		print('orgn:', piece_coord, '\n')
		'''

		# alterations on the board
		if movement[0] == '0':
			# castle
			row = None
			if self.turn == WHITE:
				row = 7
			else:
				row = 0

			if movement == '0-0':
				# king side
				if self.turn == WHITE:
					self.white_king_has_moved = True
					self.white_king_rook_has_moved = True
				else:
					self.black_king_has_moved = True
					self.black_king_rook_has_moved = True

				self.board[row][6] = self.board[row][4]
				self.board[row][4] = None

				self.board[row][5] = self.board[row][7]
				self.board[row][7] = None
			elif movement == '0-0-0':
				# queen side
				if self.turn == WHITE:
					self.white_king_has_moved = True
					self.white_queen_rook_has_moved = True
				else:
					self.black_king_has_moved = True
					self.black_queen_rook_has_moved = True

				self.board[row][2] = self.board[row][4]
				self.board[row][4] = None

				self.board[row][3] = self.board[row][0]
				self.board[row][0] = None
			else:
				raise Exception('Something unexpected went wrong. This should have been handled before')

		else:
			self.validate_move_causes_self_check(piece_coord, destination)

			# tracking the kings moves
			if movement[0] == 'K':
				if self.turn == WHITE:
					self.white_king_has_moved = True
				else:
					self.black_king_has_moved = True
			elif movement[0] == 'R':
				# for castle purposes
				# a more elegant way of doing this is changing every element of the board for classes
				# it would take a lot of effort, so I'll try this way before
				if self.turn == WHITE and piece_coord[0] == 7:
					if piece_coord[1] == 0:
						self.white_queen_rook_has_moved = True
					elif piece_coord[1] == 7:
						self.white_king_rook_has_moved = True
				elif self.turn == BLACK and piece_coord[0] == 0:
					if piece_coord[1] == 0:
						self.black_queen_rook_has_moved = True
					elif piece_coord[1] == 7:
						self.black_king_rook_has_moved = True

			self.handle_possible_pawn_upgrade(movement, piece_coord, destination)

			self.board[destination[0]][destination[1]] = self.board[piece_coord[0]][piece_coord[1]]
			self.board[piece_coord[0]][piece_coord[1]] = None

		# white did an en passant move
		if self.en_passant_flag_white:
			self.en_passant_flag_white = False
			self.board[destination[0] + 1][destination[1]] = None
		elif self.en_passant_flag_black:
			self.en_passant_flag_black = False
			self.board[destination[0] - 1][destination[1]] = None

		if self.en_passant_just_now:
			self.en_passant_just_now = False
		else:
			if self.turn == WHITE:
				self.en_passant_coord_white = None
			else:
				self.en_passant_coord_black = None

		self.moves.append(movement)

		self.turn = not self.turn

		if self.is_checkmate():
			raise Exception('Checkmate')

		return [piece_coord, destination]

	def handle_pawn_move(self, movement):
		# todo: pawn upgrade implementation (should be easy)
		destination = None
		piece_coord = None
		if 'x' in movement:
			# capture with pawn
			destination = (self.get_row(movement[3]), self.get_column(movement[2]))
			origin_column = self.get_column(movement[0])
			piece_coord = self.find_capturer_pawn(color=self.turn, destination_row=destination[0],
			                                      origin_column=origin_column)

			self.validate_capture_with_pawn(piece_coord, destination)
		else:
			# pawn move
			destination = (self.get_row(movement[1]), self.get_column(movement[0]))
			piece_coord = self.find_pawn(color=self.turn, column=destination[1], limit=destination[0])

			self.validate_pawn_move(piece_coord, destination)

		if destination is None or piece_coord is None:
			raise Exception('Something went wrong. This should not happen in any case because if this conditional is '
			                'true, other exception calls should have triggered before. Go for a walk and then try to '
			                'solve this.')

		return destination, piece_coord

	def handle_rook_move(self, movement, add):
		if self.is_normal_movement(movement, add):
			# not in the same column or row
			destination = (self.get_row(movement[2 + add]), self.get_column(movement[1 + add]))
			coords = self.find_rook(self.turn, destination)

			if len(coords) == 1:
				piece_coord = coords[0]
			elif len(coords) == 2:
				raise IlegalMoveException('Please specify which rook you want to move')
			else:
				raise Exception('Something went wrong. This should not have been called')
		elif self.is_same_row_movement(movement, add):
			# in the same row
			destination = (self.get_row(movement[3 + add]), self.get_column(movement[2 + add]))
			piece_coord = (self.get_row(movement[3 + add]), self.get_column(movement[1]))

		elif self.is_same_col_movement(movement, add):
			# in the same column
			destination = (self.get_row(movement[3 + add]), self.get_column(movement[2 + add]))
			piece_coord = (self.get_row(movement[1]), self.get_column(movement[2 + add]))
		else:
			raise IlegalMoveException('Invalid movement')

		self.validate_rook_move(piece_coord, destination, self.is_move_capture(movement))

		if destination is None or piece_coord is None:
			raise Exception('Something went wrong. This should not happen in any case because if this conditional is '
			                'true, other exception calls should have triggered before. Go for a walk and then try to '
			                'solve this.')

		return destination, piece_coord

	def handle_knight_move(self, movement, add):
		if self.is_normal_movement(movement, add):
			# not in the same row or column
			destination = (self.get_row(movement[2 + add]), self.get_column(movement[1 + add]))
			coords = self.find_knight(color=self.turn, destination=destination)

			if len(coords) == 1:
				piece_coord = coords[0]
			else:
				# checking for 0 is already done in the find_knight function
				raise IlegalMoveException('Please inform which one of the knights you want to move')
		elif self.is_same_row_movement(movement, add):
			# in the same row
			destination = (self.get_row(movement[3 + add]), self.get_column(movement[2 + add]))
			col = self.get_column(movement[1])
			coords = self.find_knight(color=self.turn, destination=destination)

			if len(coords) == 1:
				piece_coord = coords[0]
			elif len(coords) == 2:
				if coords[0][1] == col:
					piece_coord = coords[0]
				elif coords[1][1] == col:
					piece_coord = coords[1]
				else:
					raise IlegalMoveException("Couldn't find a knight with the specified command")
			else:
				raise IlegalMoveException('The number of knights found is more than two:', len(coords))
		elif self.is_same_col_movement(movement, add):
			destination = (self.get_row(movement[3 + add]), self.get_column(movement[2 + add]))
			row = self.get_row(movement[1])
			coords = self.find_knight(color=self.turn, destination=destination)

			if len(coords) == 1:
				piece_coord = coords[0]
			elif len(coords) == 2:
				if coords[0][0] == row:
					piece_coord = coords[0]
				elif coords[1][0] == row:
					piece_coord = coords[1]
				else:
					raise IlegalMoveException("Couldn't find a knight with the specified command")
			else:
				raise IlegalMoveException('The number of knights found is more than two:', len(coords))
		else:
			raise IlegalMoveException('Invalid movement')

		self.validate_knight_move(piece_coord=piece_coord, destination=destination,
		                          capture=self.is_move_capture(movement))

		if destination is None or piece_coord is None:
			raise Exception('Something went wrong. This should not happen in any case because if this conditional is '
			                'true, other exception calls should have triggered before. Go for a walk and then try to '
			                'solve this.')

		return destination, piece_coord

	def handle_bishop_move(self, movement, add):
		# there is no no need to check for anmbiguous moviments because of the nature of different square
		# colors for bishops
		destination = (self.get_row(movement[2 + add]), self.get_column(movement[1 + add]))
		piece_coord = self.find_bishop(color=self.turn, destination=destination)

		self.validate_bishop_move(piece_coord=piece_coord, destination=destination,
		                          capture=self.is_move_capture(movement))

		if destination is None or piece_coord is None:
			raise Exception('Something went wrong. This should not happen in any case because if this conditional is '
			                'true, other exception calls should have triggered before. Go for a walk and then try to '
			                'solve this.')

		return destination, piece_coord

	def handle_queen_move(self, movement, add):
		# I'll try to combine both the rook and bishop code into this one, since it seems like in the surface
		# that it'll work
		# Also it doesn't need to check for ambiguity because there is only one queen
		destination = (self.get_row(movement[2 + add]), self.get_column(movement[1 + add]))
		piece_coord = self.find_queen(color=self.turn, destination=destination)

		self.validate_queen_move(piece_coord=piece_coord, destination=destination,
		                         capture=self.is_move_capture(movement))

		if destination is None or piece_coord is None:
			raise Exception('Something went wrong. This should not happen in any case because if this conditional is '
			                'true, other exception calls should have triggered before. Go for a walk and then try to '
			                'solve this.')

		return destination, piece_coord

	def handle_king_move(self, movement, add):
		# In the same way as the queen, there is no reason to check for ambiguity because there is only one king
		destination = (self.get_row(movement[2 + add]), self.get_column(movement[1 + add]))
		piece_coord = self.find_king(color=self.turn, destination=destination)

		self.validate_king_move(piece_coord=piece_coord, destination=destination, capture=self.is_move_capture(movement))

		if destination is None or piece_coord is None:
			raise Exception('Something went wrong. This should not happen in any case because if this conditional is '
			                'true, other exception calls should have triggered before. Go for a walk and then try to '
			                'solve this.')

		return destination, piece_coord

	def handle_castle(self, movement):
		self.validate_castle_move(movement)

	def handle_possible_pawn_upgrade(self, movement, piece_coord, destination):
		if '=' in movement:
			# pawn upgrade
			if self.turn == WHITE and destination[0] != 0:
				raise IlegalMoveException('You can only upgrade the pawn in the last row')

			if self.turn == BLACK and destination[0] != 7:
				raise IlegalMoveException('You can only upgrade the pawn in the last row')

			new_char = movement[-1]
			if new_char in 'QBNR':
				piece = self.board[piece_coord[0]][piece_coord[1]]
				piece = piece[0] + new_char.lower()
				self.board[piece_coord[0]][piece_coord[1]] = piece
			else:
				raise IlegalMoveException('Invalid piece code to upgrade to')
		elif (self.turn == WHITE and destination[0] == 0) or (self.turn == BLACK and destination[0] == 7):
			raise IlegalMoveException('You need to define the piece to upgrade to')