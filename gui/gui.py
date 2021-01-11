import pygame
import pygame.freetype

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

SQUARE_SIZE = int(SCREEN_HEIGHT / 10)
BOARD_BORDER = SQUARE_SIZE

DARK_COLOR = (132, 166, 102)
LIGHT_COLOR = (255, 255, 221)
DARK_SELECTED_COLOR = (79, 162, 142)
LIGHT_SELECTED_COLOR = (150, 214, 212)


SPRITES_FOLDER = 'gui/sprites/'


class Gui:

	def __init__(self, board):
		self.board = board
		self.moves = []

		self.origin_square = None
		self.destination = None
		self.check = None

		pygame.init()
		pygame.font.init()
		self.font = pygame.font.SysFont('Ligconsolata', 24)

		self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
		self.running = True
		self.load_sprites()

	def start(self):
		while self.running:
			self.draw_board()
			pygame.display.update()

	def set_board(self, board):
		self.board = board

	def set_aditional_info(self, origin_square, destination, check):
		# all tuples of (i, j)
		self.origin_square = origin_square
		self.destination = destination
		self.check = check

	def set_moves(self, moves):
		self.moves = moves

	def add_move(self, move):
		self.moves.append(move)

	def reset_moves(self):
		self.moves = []

	def load_sprites(self):
		self.white_king = pygame.image.load(SPRITES_FOLDER + 'white_king.png').convert_alpha()
		self.white_queen = pygame.image.load(SPRITES_FOLDER + 'white_queen.png').convert_alpha()
		self.white_bishop = pygame.image.load(SPRITES_FOLDER + 'white_bishop.png').convert_alpha()
		self.white_knight = pygame.image.load(SPRITES_FOLDER + 'white_knight.png').convert_alpha()
		self.white_rook = pygame.image.load(SPRITES_FOLDER + 'white_rook.png').convert_alpha()
		self.white_pawn = pygame.image.load(SPRITES_FOLDER + 'white_pawn.png').convert_alpha()

		self.black_king = pygame.image.load(SPRITES_FOLDER + 'black_king.png').convert_alpha()
		self.black_queen = pygame.image.load(SPRITES_FOLDER + 'black_queen.png').convert_alpha()
		self.black_bishop = pygame.image.load(SPRITES_FOLDER + 'black_bishop.png').convert_alpha()
		self.black_knight = pygame.image.load(SPRITES_FOLDER + 'black_knight.png').convert_alpha()
		self.black_rook = pygame.image.load(SPRITES_FOLDER + 'black_rook.png').convert_alpha()
		self.black_pawn = pygame.image.load(SPRITES_FOLDER + 'black_pawn.png').convert_alpha()

		self.check_sprite = pygame.image.load(SPRITES_FOLDER + 'check.png').convert_alpha()

	def draw_board(self):
		next_color = LIGHT_COLOR
		for i in range(8):
			text = self.font.render(chr(i + 97), 1, pygame.Color('white'))
			center = (i * SQUARE_SIZE + SQUARE_SIZE * 3 / 2, SCREEN_HEIGHT - SQUARE_SIZE / 1.5)
			text_rect = text.get_rect(center=center)
			self.screen.blit(text, text_rect)

			text = self.font.render(str(abs(8 - i)), 1, pygame.Color('white'))
			center = (SQUARE_SIZE / 1.5, i * SQUARE_SIZE + SQUARE_SIZE * 3 / 2)
			text_rect = text.get_rect(center=center)
			self.screen.blit(text, text_rect)

			for j in range(8):
				pos = (j * SQUARE_SIZE + BOARD_BORDER, i * SQUARE_SIZE + BOARD_BORDER)

				if (self.origin_square is not None and (i, j) == self.origin_square) or (self.destination is not None and (i, j) == self.destination):
					if next_color == LIGHT_COLOR:
						color = LIGHT_SELECTED_COLOR
					else:
						color = DARK_SELECTED_COLOR
				else:
					color = next_color

				rect = (pos[0], pos[1], SQUARE_SIZE, SQUARE_SIZE)
				pygame.draw.rect(self.screen, color, rect)

				if self.check is not None and (i, j) == self.check:
					pic = pygame.transform.smoothscale(self.check_sprite, (SQUARE_SIZE, SQUARE_SIZE))
					self.screen.blit(pic, (pos[0], pos[1]))

				piece = self.board[i][j]
				if piece is not None:
					sprite = None
					if piece[0] == 'w':
						if piece[1] == 'p':
							sprite = self.white_pawn
						elif piece[1] == 'r':
							sprite = self.white_rook
						elif piece[1] == 'n':
							sprite = self.white_knight
						elif piece[1] == 'b':
							sprite = self.white_bishop
						elif piece[1] == 'q':
							sprite = self.white_queen
						elif piece[1] == 'k':
							sprite = self.white_king
						else:
							raise Exception('This should not happen')
					else:
						if piece[1] == 'p':
							sprite = self.black_pawn
						elif piece[1] == 'r':
							sprite = self.black_rook
						elif piece[1] == 'n':
							sprite = self.black_knight
						elif piece[1] == 'b':
							sprite = self.black_bishop
						elif piece[1] == 'q':
							sprite = self.black_queen
						elif piece[1] == 'k':
							sprite = self.black_king
						else:
							raise Exception('This should not happen')

					if sprite is not None:
						pic = pygame.transform.smoothscale(sprite, (SQUARE_SIZE, SQUARE_SIZE))
						self.screen.blit(pic, (pos[0], pos[1]))
					else:
						raise Exception('Null sprite')

				if next_color == LIGHT_COLOR:
					next_color = DARK_COLOR
				else:
					next_color = LIGHT_COLOR

			if next_color == LIGHT_COLOR:
				next_color = DARK_COLOR
			else:
				next_color = LIGHT_COLOR

	def draw_moves(self):
		pass