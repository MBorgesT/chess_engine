file = open('airthingsmastp20.pgn', 'r', encoding='utf-8')
txt = file.read()
file.close()

file = open('games.txt', 'w')

flag = True
while flag:
    start = txt.find('\n\n') + 2
    txt = txt[start:]

    end = txt.find('[')
    if end < 0:
        end = len(txt)
        flag = False

    game = txt[:(end - 2)]
    txt = txt[end:]

    game = game.replace('\n', ' ')
    moves = game.split(' ')

    result = moves[-1]
    moves = moves[:-1]

    new_moves = []
    for i in range(len(moves)):
        if i % 3 != 0:
            new_moves.append(moves[i])

    moves = new_moves
    moves.append(result)
    
    file.write(' '.join(moves) + '\n')
    
file.close()