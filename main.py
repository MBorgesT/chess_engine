from game import Game
from draw_board import draw_board
from time import time

def move_piece(movement):
    start = time()
    res = game.move_piece(movement)
    end = time()
    print('time:', end - start)
    draw_board(game.get_board(), origin_square=res[0], destination_square=res[1])

game = Game()
draw_board(game.get_board())

print(game.is_checkmate())

'''
while True:
    move_piece(input())
'''
