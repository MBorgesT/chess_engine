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

	def get_board(self):
		return self.board

	def print_board(self):
		for row in self.board:
			print(row)

	def is_piece_white(self, piece):
		return piece[0] == 'w'
	
	def is_piece_black(self, piece):
		return piece[0] == 'b'

	def validate_move_generates_check(self, piece_coord, destination):
		raise Exception('Not yet implemented')

	def validate_coord_out_of_board(self, coord):
		if coord[0] < 0 or coord[0] > 8 or coord[1] < 0 or coord[1] > 8:
			raise ValueError('Coordinates out of boundries')

	def validate_pawn_move(self, piece_coord, destination):
		# destination and piece_coord: (row, column)
		piece = self.board[piece_coord[0]][piece_coord[1]]

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
				if (self.is_piece_white(piece) and self.en_passant_coord_black != destination) or (self.is_piece_black(piece) and self.en_passant_coord_white != destination))
				raise ValueError('There is no piece in the destination square to capture')
			elif destination_piece[0] == 'w':
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

	def move_piece(self, moviment):
		destination = None
		piece_coord = None

		if moviment[0].isupper():
			raise Exception('Not implemented yet')

		else:
			# pawn moviment
			if 'x' in moviment:
				raise Exception('Not implemented yet')
			else:
				# pawn move
				destination = (abs(int(moviment[1]) - 8), ord(moviment[0]) - 97)
				print('dest:', destination)
				if self.turn == self.WHITE:
					for i in range(7, destination[0], -1):
						piece = self.board[i][destination[1]] 
						if piece is not None and ((self.turn == self.WHITE and self.is_piece_white(piece)) or (self.turn == self.BLACK and self.is_piece_black(piece))) :
							piece_coord = (i, destination[1])
				print('piec:', piece_coord)
				
				self.validate_pawn_move(piece_coord, destination)

		self.board[destination[0]][destination[1]] = self.board[piece_coord[0]][piece_coord[1]]
		self.board[piece_coord[0]][piece_coord[1]] = None

		if self.turn == self.WHITE:
			self.en_passant_coord_white = None
		else:
			self.en_passant_coord_black = None

		self.turn = not self.turn