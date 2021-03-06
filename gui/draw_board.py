from PIL import Image, ImageDraw

DARK_COLOR = (132, 166, 102)
LIGHT_COLOR = (255, 255, 221)
DARK_SELECTED_COLOR = (79, 162, 142)
LIGHT_SELECTED_COLOR = (150, 214, 212)

SQUARE_SIZE = 200

CHECK = Image.open('gui/sprites/check.png').convert('RGBA')

WK = Image.open('gui/sprites/white_king.png').convert('RGBA')
WQ = Image.open('gui/sprites/white_queen.png').convert('RGBA')
WR = Image.open('gui/sprites/white_rook.png').convert('RGBA')
WB = Image.open('gui/sprites/white_bishop.png').convert('RGBA')
WN = Image.open('gui/sprites/white_knight.png').convert('RGBA')
WP = Image.open('gui/sprites/white_pawn.png').convert('RGBA')

BK = Image.open('gui/sprites/black_king.png').convert('RGBA')
BQ = Image.open('gui/sprites/black_queen.png').convert('RGBA')
BR = Image.open('gui/sprites/black_rook.png').convert('RGBA')
BB = Image.open('gui/sprites/black_bishop.png').convert('RGBA')
BN = Image.open('gui/sprites/black_knight.png').convert('RGBA')
BP = Image.open('gui/sprites/black_pawn.png').convert('RGBA')

pieces_images = dict()

pieces_images.update({'wk': WK})
pieces_images.update({'wq': WQ})
pieces_images.update({'wr': WR})
pieces_images.update({'wb': WB})
pieces_images.update({'wn': WN})
pieces_images.update({'wp': WP})

pieces_images.update({'bk': BK})
pieces_images.update({'bq': BQ})
pieces_images.update({'br': BR})
pieces_images.update({'bb': BB})
pieces_images.update({'bn': BN})
pieces_images.update({'bp': BP})


def draw_board(board, origin_square=None, destination_square=None, check=None):

	def get_xy(i, j):
		return (
			j * SQUARE_SIZE,
			i * SQUARE_SIZE,
			j * SQUARE_SIZE + SQUARE_SIZE,
			i * SQUARE_SIZE + SQUARE_SIZE
		)
	
	def get_piece_image(square):
		if square is None:
			return None
		else:
			return pieces_images[square]


	next_color = LIGHT_COLOR

	img = Image.new('RGBA', (SQUARE_SIZE * 8, SQUARE_SIZE * 8))
	draw = ImageDraw.Draw(img)

	for i in range(8):
		for j in range(8):
			color = None
			if (i, j) == origin_square or (i, j) == destination_square:
				if next_color == LIGHT_COLOR:
					color = LIGHT_SELECTED_COLOR
				else:
					color = DARK_SELECTED_COLOR
			else:
				color = next_color

			draw.rectangle(xy=get_xy(i, j), fill=color)

			if check is not None and check[0] == i and check[1] == j:
				img.alpha_composite(CHECK, dest=(j * SQUARE_SIZE, i * SQUARE_SIZE))

			piece = get_piece_image(board[i][j])
			if piece is not None:
				img.alpha_composite(piece, dest=(j * SQUARE_SIZE, i * SQUARE_SIZE))

			if next_color == LIGHT_COLOR:
				next_color = DARK_COLOR
			else:
				next_color = LIGHT_COLOR
		
		if next_color == LIGHT_COLOR:
			next_color = DARK_COLOR
		else:
			next_color = LIGHT_COLOR

	img.save('board.png')
