class Game:

	def __init__(self):
		self.board = [
			['br', 'bn', 'bb', 'bq', 'bk', 'bb', 'bn', 'br'],
			['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
			[None, None, None, None, None, None, None, None],
			[None, None, None, None, None, None, None, None],
			[None, None, None, 'bp', None, None, None, None],
			[None, None, None, 'wr', None, None, None, None],
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

	def find_rook(self, color, destination):
		# going throw columns
		for col in range(8):
			piece = self.board[destination[0]][col]
			if piece is not None and piece[1] == 'r' and ((self.is_piece_white(piece) and color == self.WHITE) 
				or (self.is_piece_black(piece) and color == self.BLACK)):
				return (destination[0], col)

		# going throw rows
		for row in range(8):
			piece = self.board[row][destination[1]]
			if piece is not None and piece[1] == 'r' and ((self.is_piece_white(piece) and color == self.WHITE) 
				or (self.is_piece_black(piece) and color == self.BLACK)):
				return (row, destination[1])

		raise Exception('Rook not found. Check for bugs')

	def find_knight(self, color, destination):
		raise Exception('Not implemented yet')

	def validate_move_generates_check(self, piece_coord, destination):
		raise Exception('Not yet implemented')

	def validate_coord_out_of_board(self, coord):
		if coord[0] < 0 or coord[0] > 8 or coord[1] < 0 or coord[1] > 8:
			raise ValueError('Coordinates out of boundries')

	def validate_pawn_move(self, piece_coord, destination):
		# destination and piece_coord: (row, column)
		piece = self.board[piece_coord[0]][piece_coord[1]]

		if piece is not None:
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
				elif row_distance != 1:
					raise ValueError('Wrong row distance', row_distance)
			elif piece[1] == 'b':
				# check if distance is correct
				if row_distance == -2:
					if piece_coord[0] != 1:
						raise ValueError('Wrong row distance:', row_distance)
					elif self.board[piece_coord[0] - 1][piece_coord[1]] is not None:
						raise ValueError('There is another piece in the way')

					self.en_passant_coord_black = (2, piece_coord[1])
				elif row_distance != -1:
					raise ValueError('Wrong row distance', row_distance)

		else:

			raise ValueError('This is not a capture move')

	def validate_capture_with_pawn(self, piece_coord, destination):
		# destination and piece_coord: [row, column]
		piece = self.board[piece_coord[0]][piece_coord[1]]

		if piece is not None:
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
			elif self.get_piece_color(destination_piece) == self.get_piece_color(piece):
				raise ValueError("You can't capture your own piece")

			if piece[0] == 'w':
				# check if distance is correct
				if piece_coord[1] - destination[1] != 1:
					raise ValueError('Wrong row distance')
			elif piece[1] == 'b':
				# check if distance is correct
				if piece_coord[1] - destination[1] != -1:
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

		start = None
		end = None

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
		if capture and self.get_piece_color(destination_piece) == self.get_piece_color(piece):
			raise ValueError("You can't capture your own piece")
		if not capture and destination_piece is not None:
			raise ValueError("That is a place where you're trying to move. Try the capture move")

	def move_piece(self, movement):
		destination = None
		piece_coord = None

		if movement[0].isupper():
			# if the movement is of capture, it's just easier if we shift the reading one character to the right
			add = 0
			if 'x' in movement:
				add = 1

			if movement[0] == 'R':
				# rook
				if self.is_normal_movement(movement, add):
					# not in the same column or row
					destination = (self.get_row(movement[2 + add]), self.get_column(movement[1 + add]))

					count = 0
					for row in range(8):
						piece = self.board[row][destination[1]]
						if piece is not None and piece[1] == 'r' and self.get_piece_color(piece) == self.turn:
							count += 1
					for col in range(8):
						piece = self.board[destination[0]][col]
						if piece is not None and piece[1] == 'r' and self.get_piece_color(piece) == self.turn:
							count += 1

					if count > 1:
						raise ValueError('Please inform which rook you want to move')

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

				is_capture = lambda move: 'x' in move
				self.validate_rook_move(piece_coord, destination, is_capture(movement))
			
			elif movement[0] == 'N':
				# knight
				if self.is_normal_movement(movement, add):
					raise Exception('Not implemented yet')


		else:
			# pawn
			if 'x' in movement:
				# capture with pawn
				destination = (self.get_row(movement[3]), self.get_column(movement[2]))
				origin_column = self.get_column(movement[0])
				piece_coord = self.find_pawn(color=self.turn, column=origin_column, limit=destination[0])

				self.validate_capture_with_pawn(piece_coord, destination)
			else:
				# pawn move
				destination = (self.get_row(movement[1]), self.get_column(movement[0]))
				piece_coord = self.find_pawn(color=self.turn, column=destination[1], limit=destination[0])

				self.validate_pawn_move(piece_coord, destination)

		print('dest:', destination)
		print('orgn:', piece_coord)

		self.board[destination[0]][destination[1]] = self.board[piece_coord[0]][piece_coord[1]]
		self.board[piece_coord[0]][piece_coord[1]] = None

		if self.turn == self.WHITE:
			self.en_passant_coord_white = None
		else:
			self.en_passant_coord_black = None

		self.moves.append(movement)

		self.turn = not self.turn

		return [piece_coord, destination]