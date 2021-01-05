from game import Game
from draw_board import draw_board

game = Game()

draw_board(game.get_board())

input()
game.move_piece('e4')
draw_board(game.get_board())

game.print_board()

input()
game.move_piece('e5')
draw_board(game.get_board())