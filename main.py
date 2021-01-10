from game import Game
from draw_board import draw_board
from time import time, sleep

def move_piece(movement):
    start = time()
    res = game.move_piece(movement)
    end = time()
    print('time:', end - start)
    #draw_board(game.get_board(), origin_square=res[0], destination_square=res[1])
    #input()

file = open('games.txt', 'r')
games = file.readlines()
file.close()

file = open('first_game_not_tested.txt', 'r')
first_game = int(file.read())
file.close()

for i in range(first_game, len(games)):
    game = games[i]
    moves = game.split(' ')
    result = moves[-1]
    moves = moves[:-1]

    game = Game()
    draw_board(game.get_board())

    for j in range(len(moves)):
        move_piece(moves[j])

    print('result:', result)
    #input()

    i += 1

    file = open('first_game_not_tested.txt', 'w')
    file.write(str(i))
    file.close()