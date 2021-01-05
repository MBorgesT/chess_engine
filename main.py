from game import Game
from draw_board import draw_board

game = Game()

draw_board(game.get_board())

input()

origin_square = (6, 4)
destination_square = (4, 4)

game.move_pawn(origin_square, destination_square)

draw_board(game.get_board(), origin_square, destination_square)