from math import sin, cos, pi
from copy import deepcopy

# TODO:
#   implement castle
#   implement pawn upgrade

class CheckException(Exception):
	pass

class IlegalMoveException(Exception):
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
			['br', 'bn', 'bb', 'bq', 'bk', 'bb', None, None],
			['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'wp', 'wk'],
			[None, None, None, None, None, None, None, None],
			[None, None, None, None, None, None, None, None],
			[None, None, None, None, None, None, None, None],
			[None, None, None, None, None, None, None, None],
			['wp', 'wp', 'wp', 'wp', 'wp', 'wp', None, 'wp'],
			['wr', 'wn', 'wb', 'wq', None, 'wb', 'wn', 'wr']
		]

		self.moves = []

		self.turn = WHITE

		self.en_passant_coord_white = None
		self.en_passant_coord_black = None

		self.en_passant_flag_white = False
		self.en_passant_flag_black = False

		self.en_passant_just_now = False

		self.white_king_coord = None
		self.black_king_coord = None

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

	def raise_move_causes_self_check(self):
		raise CheckException('This move causes yourself a check')

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

	def validate_move_causes_self_check(self, piece_coord, destination):
		board_copy = deepcopy(self.board)

		king_coord = None
		king_str = None

		if self.turn == WHITE:
			king_str = 'wk'
		else:
			king_str = 'bk'

		# maybe change this to go reverse in the rows if the king is white for performance
		for i in range(8):
			found = False
			for j in range(8):
				if self.board[i][j] == king_str:
					king_coord = (i, j)
					found = True
					break
			if found:
				break

		# alterations on the board
		self.board[destination[0]][destination[1]] = self.board[piece_coord[0]][piece_coord[1]]
		self.board[piece_coord[0]][piece_coord[1]] = None

		# rook part
		try:
			e_rook_coords = self.find_rook(not self.turn, king_coord)
			for c in e_rook_coords:
				self.validate_rook_move(c, king_coord, True)

			self.raise_move_causes_self_check()
		except CheckException:
			self.raise_move_causes_self_check()
		except:
			# Couldn't capture
			None

		# knight part
		try:
			e_knight_coords = self.find_knight(not self.turn, king_coord)
			for c in e_knight_coords:
				self.validate_knight_move(c, king_coord, True)

			self.raise_move_causes_self_check()
		except CheckException:
			self.raise_move_causes_self_check()
		except:
			# Couldn't capture
			pass

		# bishop part
		try:
			e_bishop_coord = self.find_bishop(not self.turn, king_coord)
			self.validate_bishop_move(e_bishop_coord, king_coord, True)
			self.raise_move_causes_self_check()
		except CheckException:
			print('hello')
			self.raise_move_causes_self_check()
		except:
			# Couldn't capture
			pass

		# queen part
		try:
			e_queen_coord = self.find_queen(not self.turn, king_coord)
			self.validate_queen_move(e_queen_coord, king_coord, True)
			self.raise_move_causes_self_check()
		except CheckException:
			self.raise_move_causes_self_check()
		except:
			# Couldn't capture
			None

		# king part
		try:
			e_king_coord = None

			if self.turn == WHITE:
				e_king_coord = self.black_king_coord
			else:
				e_king_coord = self.white_king_coord

			self.validate_king_move(e_king_coord, king_coord, True)
			self.raise_move_causes_self_check()
		except CheckException:
			self.raise_move_causes_self_check()
		except:
			# Couldn't capture
			None

		# it's needed to validate the pawns manually here because the other functions don't work in this case
		try:
			if self.turn == WHITE:
				king_col = king_coord[1]
				if king_col - 1 >= 0:
					possible_pawn = self.board[king_coord[0] - 1][king_col - 1]
					if possible_pawn is not None and possible_pawn == 'bp':
						self.raise_move_causes_self_check()
				if king_col + 1 <= 8:
					possible_pawn = self.board[king_coord[0] - 1][king_col + 1]
					if possible_pawn is not None and possible_pawn == 'bp':
						self.raise_move_causes_self_check()
			else:
				king_col = king_coord[1]
				if king_col - 1 >= 0:
					possible_pawn = self.board[king_coord[0] + 1][king_col - 1]
					if possible_pawn is not None and possible_pawn == 'wp':
						self.raise_move_causes_self_check()
				if king_col + 1 <= 8:
					possible_pawn = self.board[king_coord[0] + 1][king_col + 1]
					if possible_pawn is not None and possible_pawn == 'wp':
						self.raise_move_causes_self_check()
		except CheckException:
			self.raise_move_causes_self_check()
		except:
			# Couldn't captur
			pass

		# going back to normal
		self.board = deepcopy(board_copy)

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
		elif piece_coord[0] == destination[0] or piece_coord[0] == destination[0]:
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

	# -----------------------------------------------------------------------------------------------------------------
	#                                 ALGEBRAIC NOTATION TRANSLATORS AND MOVE HANDLER
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
				raise IlegalMoveException('This command is invalid')
		elif movement[0] == 'x' or 97 <= ord(movement[0]) <= 104:
			# pawn
			destination, piece_coord = self.handle_pawn_move(movement)
		else:
			raise IlegalMoveException('This command is invalid')

		self.validate_move_causes_self_check(piece_coord, destination)

		print('move:', movement)
		print('dest:', destination)
		print('orgn:', piece_coord, '\n')

		# tracking the kings moves
		if movement[0] == 'K':
			if self.turn == WHITE:
				self.white_king_coord = destination
			else:
				self.black_king_coord = destination

		self.handle_possible_pawn_upgrade(movement, piece_coord, destination)

		# alterations on the board
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

		#self.turn = not self.turn

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