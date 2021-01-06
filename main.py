from game import Game
from draw_board import draw_board

def move_piece(movement):
    res = game.move_piece(movement)
    draw_board(game.get_board(), origin_square=res[0], destination_square=res[1])

game = Game()
draw_board(game.get_board())

while True:
    move_piece(input())

'''
move_piece('Nh3')
move_piece('Ng5')
move_piece('Nxf7')
move_piece('Nd6')
move_piece('Nc4')
move_piece('Ne3')
move_piece('Nc3')
move_piece('Ned5')
move_piece('Nxc7')
move_piece('N3xb5')
'''
