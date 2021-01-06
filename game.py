from math import sin, cos, pi

class Game:

	def __init__(self):
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

		self.moves = []

		# True == white; False == black
		self.WHITE = True
		self.BLACK = False
		self.turn = self.WHITE

		self.en_passant_coord_white = None
		self.en_passant_coord_black = None

		self.en_passant_flag_white = False
		self.en_passant_flag_black = False

		self.en_passant_just_now = False

	def get_board(self):
		return self.board

	def print_board(self):
		for row in self.board:
			print(row)

	def get_piece_color(self, piece):
		if piece[0] == 'w':
			return self.WHITE
		elif piece[0] == 'b':
			return self.BLACK
		else:
			raise Exception("It's not possible to identify the piece's color")

	def get_column(self, char):
		return ord(char) - 97

	def get_row(self, digit):
		return abs(int(digit) - 8)

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

	def find_pawn(self, color, column, limit):
		piece_coord = None
		if color == self.WHITE:
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
		if color == self.WHITE:
			return (destination_row + 1, origin_column)
		else:
			return (destination_row - 1, origin_column)

	def find_rook(self, color, destination):
		found = False
		rook_coord = None

		# going throw columns
		for col in range(8):
			piece = self.board[destination[0]][col]
			if piece is not None and piece[1] == 'r' and self.get_piece_color(piece) == color:
				if not found:
					found = True
					rook_coord = (destination[0], col)
				else:
					raise ValueError('Please inform which rook you want to move')

		# going throw rows
		for row in range(8):
			piece = self.board[row][destination[1]]
			if piece is not None and piece[1] == 'r' and self.get_piece_color(piece) == color:
				if not found:
					found = True
					rook_coord = (row, destination[1])
				else:
					raise ValueError('Please inform which rook you want to move')

		if found:
			return rook_coord
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
			self.print_board()
			raise ValueError('No knight was found')

	def validate_move_generates_check(self, piece_coord, destination):
		raise Exception('Not yet implemented')

	def validate_coord_out_of_board(self, coord):
		return 0 <= coord[0] <= 7 and 0 <= coord[1] <= 7

	def validate_pawn_move(self, piece_coord, destination):
		# destination and piece_coord: (row, column)
		piece = self.board[piece_coord[0]][piece_coord[1]]

		if piece is None:
			raise ValueError('There is no piece in the origin square')

		if piece[1] != 'p':
			raise ValueError('Wrong piece passed as parameter:', piece)

		# check if same row
		if piece_coord[1] == destination[1]:

			# check if column distance is ok
			if abs(piece_coord[1] - destination[1]) != 0:
				raise ValueError('Column distance is invalid')

			# check if there is any piece in the destination
			destination_piece = self.board[destination[0]][destination[1]]
			if destination_piece is not None:
				raise ValueError('There is a piece in the destination square')

			row_distance = piece_coord[0] - destination[0]

			if piece[0] == 'w':
				# check if distance is correct
				if row_distance == 2:
					if piece_coord[0] != 6:
						raise ValueError('Wrong row distance:', row_distance)
					elif self.board[piece_coord[0] - 1][piece_coord[1]] is not None:
						raise ValueError('There is another piece in the way')

					self.en_passant_coord_white = (5, piece_coord[1])
					self.en_passant_just_now = True
				elif row_distance != 1:
					raise ValueError('Wrong row distance', row_distance)
			elif piece[0] == 'b':
				# check if distance is correct
				if row_distance == -2:
					if piece_coord[0] != 1:
						raise ValueError('Wrong row distance:', row_distance)
					elif self.board[piece_coord[0] + 1][piece_coord[1]] is not None:
						raise ValueError('There is another piece in the way')

					self.en_passant_coord_black = (2, piece_coord[1])
					self.en_passant_just_now = True
				elif row_distance != -1:
					raise ValueError('Wrong row distance', row_distance)

		else:

			raise ValueError('This is not a capture move')

	def validate_capture_with_pawn(self, piece_coord, destination):
		# destination and piece_coord: [row, column]
		piece = self.board[piece_coord[0]][piece_coord[1]]

		if piece is None:
			raise ValueError('There is no piece in the origin square')

		if piece[1] != 'p':
			raise ValueError('Wrong piece passed as parameter:', piece)

		# check if different row
		if piece_coord[1] != destination[1]:

			# check if column distance is ok
			if abs(piece_coord[1] - destination[1]) != 1:
				raise ValueError('Column distance is invalid')

			# check if there is enemy piece in the destination
			destination_piece = self.board[destination[0]][destination[1]]
			if destination_piece is None:
				# en passant possibility
				if (self.is_piece_white(piece) and self.en_passant_coord_black != destination) or (
						self.is_piece_black(piece) and self.en_passant_coord_white != destination):
					raise ValueError('There is no piece in the destination square to capture')
				else:
					# set a flag to sign on move_piece function that a en passant was done
					if self.is_piece_white(piece):
						self.en_passant_flag_white = True
					else:
						self.en_passant_flag_black = True
			elif self.get_piece_color(destination_piece) == self.get_piece_color(piece):
				raise ValueError("You can't capture your own piece")

			if piece[0] == 'w':
				# check if distance is correct
				if piece_coord[0] - destination[0] != 1:
					raise ValueError('Wrong row distance')
			elif piece[0] == 'b':
				# check if distance is correct
				if piece_coord[0] - destination[0] != -1:
					raise ValueError('Wrong row distance')
			else:
				raise ValueError('Wrong color passed as parameter:', piece)

		else:

			raise ValueError('This is not a capture move')

	def validate_rook_move(self, piece_coord, destination, capture):
		# destination and piece_coord: (row, column)
		piece = self.board[piece_coord[0]][piece_coord[1]]

		if piece is None:
			raise ValueError('There is no piece in the origin square')

		if piece[1] != 'r':
			raise ValueError('Wrong piece passed as parameter:', piece)

		if piece_coord[0] != destination[0] and piece_coord[1] != destination[1]:
			raise ValueError('Piece not in the same row or column as destination')

		if piece_coord[0] == destination[0] and piece_coord[1] == destination[1]:
			raise ValueError("You can't move to the same square")

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
					raise ValueError('There are other pieces between the origin and destination')
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
					raise ValueError('There are other pieces between the origin and destination')

		destination_piece = self.board[destination[0]][destination[1]]
		if capture:
			if destination_piece is None:
				raise ValueError('There is no piece in the square to be captured')
			if self.get_piece_color(destination_piece) == self.get_piece_color(piece):
				raise ValueError("You can't capture your own piece")
		if not capture and destination_piece is not None:
			raise ValueError("That is a place where you're trying to move. Try the capture move")

	def validate_knight_move(self, piece_coord, destination, capture):
		# destination and piece_coord: (row, column)
		piece = self.board[piece_coord[0]][piece_coord[1]]

		if piece is None:
			raise ValueError('There is no piece in the origin square')

		if piece[1] != 'n':
			raise ValueError('Wrong piece passed as parameter:', piece)

		destination_piece = self.board[destination[0]][destination[1]]
		if capture:
			if destination_piece is None:
				raise ValueError('There is no piece in the square to be captured')
			if self.get_piece_color(destination_piece) == self.get_piece_color(piece):
				raise ValueError("You can't capture your own piece")
		if not capture and destination_piece is not None:
			raise ValueError("That is a place where you're trying to move. Try the capture move")

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
				if self.is_normal_movement(movement, add):
					# not in the same column or row
					destination = (self.get_row(movement[2 + add]), self.get_column(movement[1 + add]))
					piece_coord = self.find_rook(self.turn, destination)
				elif self.is_same_row_movement(movement, add):
					# in the same row
					destination = (self.get_row(movement[3 + add]), self.get_column(movement[2 + add]))
					piece_coord = (self.get_row(movement[3 + add]), self.get_column(movement[1]))

				elif self.is_same_col_movement(movement, add):
					# in the same column
					destination = (self.get_row(movement[3 + add]), self.get_column(movement[2 + add]))
					piece_coord = (self.get_row(movement[1]), self.get_column(movement[2 + add]))
				else:
					raise ValueError('Invalid movement')

				self.validate_rook_move(piece_coord, destination, self.is_move_capture(movement))
			
			elif movement[0] == 'N':
				# knight
				if self.is_normal_movement(movement, add):
					# not in the same row or column
					destination = (self.get_row(movement[2 + add]), self.get_column(movement[1 + add]))
					coords = self.find_knight(color=self.turn, destination=destination)

					if len(coords) == 1:
						piece_coord = coords[0]
					else:
						# checking for 0 is already done in the find_knight function
						raise ValueError('Please inform which one of the knights you want to move')
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
							raise ValueError("Couldn't find a knight with the specified command")
					else:
						raise ValueError('The number of knights found is more than two:', len(coords))
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
							raise ValueError("Couldn't find a knight with the specified command")
					else:
						raise ValueError('The number of knights found is more than two:', len(coords))
				else:
					raise ValueError('Invalid movement')

				self.validate_knight_move(piece_coord=piece_coord, destination=destination, capture=self.is_move_capture(movement))

			elif movement[1] == 'b':
				# bishop
				# there is no no need to check for anmbiguous moviments because of the nature of different square
				# colors for bishops

		else:
			# pawn
			if 'x' in movement:
				# capture with pawn
				destination = (self.get_row(movement[3]), self.get_column(movement[2]))
				origin_column = self.get_column(movement[0])
				piece_coord = self.find_capturer_pawn(color=self.turn, destination_row=destination[0], origin_column=origin_column)

				self.validate_capture_with_pawn(piece_coord, destination)
			else:
				# pawn move
				destination = (self.get_row(movement[1]), self.get_column(movement[0]))
				piece_coord = self.find_pawn(color=self.turn, column=destination[1], limit=destination[0])

				self.validate_pawn_move(piece_coord, destination)


		print('move:', movement)
		print('dest:', destination)
		print('orgn:', piece_coord, '\n')

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
			if self.turn == self.WHITE:
				self.en_passant_coord_white = None
			else:
				self.en_passant_coord_black = None

		self.moves.append(movement)

		#self.turn = not self.turn

		return [piece_coord, destination]