from game import Game
from draw_board import draw_board
from time import time, sleep

def move_piece(movement):
    start = time()
    res = game.move_piece(movement)
    end = time()
    print('time:', end - start)
    draw_board(game.get_board(), origin_square=res[0], destination_square=res[1])
    #sleep(1)

file = open('games.txt', 'r')
games = file.readlines()
file.close()

i = 0
for game in games:
    moves = game.split(' ')
    result = moves[-1]
    moves = moves[:-1]

    game = Game()
    draw_board(game.get_board())

    for move in moves:
        move_piece(move)

    print('result:', result)
    sleep(5)

    i += 1