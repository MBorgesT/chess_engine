from game import Game
from draw_board import draw_board

def move_piece(moviment):
    input()
    game.move_piece(moviment)
    draw_board(game.get_board())
    game.print_board()

game = Game()

draw_board(game.get_board())

move_piece('Rbc4')
