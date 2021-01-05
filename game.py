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
		self.next_turn = True

	def get_board(self):
		return self.board

	def print_board(self):
		for row in self.board:
			print(row)

	def validate_move_generates_check(piece_coord, destination):
		raise Exception('Not yet implemented')

	def validate_coord_out_of_board(self, coord):
		if coord[0] < 0 or coord[0] > 8 or coord[1] < 0 or coord[1] > 8:
			raise ValueError('Coordinates out of boundries')

	'''
	def move_piece(moviment):
		if moviment[0].isupper():
			# not pawn moviment
			print(moviment[0])
		else:
			# pawn moviment
			if 'x' in moviment:
				# pawn capture
			else:
				# pawn move
	'''
	def move_pawn(self, piece_coord, destination):
		# destination and piece_coord: [row, column]
		piece = self.board[piece_coord[0]][piece_coord[1]]

		if piece[1] != 'p':
			raise ValueError('Wrong piece passed as parameter:', piece)

		# check if same row
		if piece_coord[1] == destination[1]:

			# check if column distance is ok
			if abs(piece_coord[1] - destination[1]) != 0:
				raise ValueError('Column distance is invalid')

			 # check if there is enemy piece in the destination
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
				elif row_distance != 1:
					raise ValueError('Wrong row distance', row_distance)
					

			elif piece[1] == 'b':
				# check if distance is correct
				if piece_coord[1] - destination[1] != -1:
					raise ValueError('Wrong row distance')

			self.board[destination[0]][destination[1]] = self.board[piece_coord[0]][piece_coord[1]]
			self.board[piece_coord[0]][piece_coord[1]] = None

		else:

			raise ValueError('This is not a capture move')

	def capture_with_pawn(self, piece_coord, destination):
		# todo: implement an passant

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


			self.board[destination[0]][destination[1]] = self.board[piece_coord[0]][piece_coord[1]]
			self.board[piece_coord[0]][piece_coord[1]] = None

		else:

			raise ValueError('This is not a capture move')
