from game import Game
from draw_board import draw_board

def move_piece(movement):
    res = game.move_piece(movement)
    draw_board(game.get_board(), origin_square=res[0], destination_square=res[1])

game = Game()
draw_board(game.get_board())

while True:
    move_piece(input())