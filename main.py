from game import Game
from draw_board import draw_board

def move_piece(moviment):
    input()
    res = game.move_piece(moviment)
    draw_board(game.get_board(), origin_square=res[0], destination_square=res[1])

game = Game()
draw_board(game.get_board())

move_piece('a3')
move_piece('d4')
move_piece('Rxbd4')