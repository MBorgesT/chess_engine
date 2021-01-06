from game import Game
from draw_board import draw_board

def move_piece(movement):
    input()
    res = game.move_piece(movement)
    draw_board(game.get_board(), origin_square=res[0], destination_square=res[1])

game = Game()
draw_board(game.get_board())

move_piece('e4')
move_piece('a5')
move_piece('e5')
move_piece('f5')
move_piece('exf6')