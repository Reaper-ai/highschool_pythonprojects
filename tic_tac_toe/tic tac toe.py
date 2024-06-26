d = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9}

board = '''
         |     |
      {}  |  {}  | {}
    _____|_____|_____
         |     |
      {}  |  {}  | {}
    _____|_____|_____
         |     |
      {}  |  {}  | {}
         |     |
         '''.format(d[1], d[2], d[3], d[4], d[5], d[6], d[7], d[8], d[9])

print(board)


def update(d):
    board = '''
         |     |
      {}  |  {}  | {}
    _____|_____|_____
         |     |
      {}  |  {}  | {}
    _____|_____|_____
         |     |
      {}  |  {}  | {}
         |     |
         '''.format(d[1], d[2], d[3], d[4], d[5], d[6], d[7], d[8], d[9])

    return print(board)


print('welcome to tic tac toe')

run = True
def restart():  #start and restart game
    print('start a new game ?')
    global start
    start = input('enter [y/n] for yes or no: ')
    return start

start = 'y'
count = 0  # turn counter
while run:
    d = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9}

    if start == 'n':
        print('see you later')
        break

    if start == 'y': # main loop
        print('player 1: X')
        print('player 2: O')
        print('enter the digit of the tile you want to make a move on')
        for i in range(0,17,2):  # subs loop
            w = False
            turn = Turn =  True
            x = "X"
            o = 'O'



            if  count >= 5:  # win check for player 2
                if d[1] == d[2] == d[3] == o or d[4] == d[5] == d[6] == o or d[7] == d[8] == d[9] == o:
                    print(' player 2 WON')
                    w = True
                    break
                elif d[1] == d[4] == d[7] == o or d[2] == d[5] == d[8] == o or d[3] == d[6] == d[9] == o:
                    print(' player 2 WON')
                    w = True
                    break
                elif d[1] == d[5] == d[9] == o or d[3] == d[5] == d[7] == o:
                    print(' player 2 WON')
                    w = True
                    break

            while turn: # player 1 turn
                if w :
                    break
                player1 = int(input('player 1: '))
                if player1 in d and d[player1] != 'X' or 'O':
                    d[player1] = 'X'
                    turn = False
                    update(d)
                    count += 1
                else:
                    print('invalid move')
                    update(d)


            if count >= 5:   #win check for player 1
                if d[1] == d[2] == d[3] == x or d[4] == d[5] == d[6] == x or d[7] == d[8] == d[9] == x:
                    print(' player 1 WON')
                    w = True
                    break
                elif d[1] == d[4] == d[7] == x or d[2] == d[5] == d[8] == x or d[3] == d[6] == d[9] == x:
                    print(' player 1 WON')
                    w = True
                    break
                elif d[1] == d[5] == d[9] == x or d[3] == d[5] == d[7] == x:
                    print(' player 1 WON')
                    w = True
                    break

            if count == 9:  # check for draw
                print('draw')
                break

            while Turn:  # player 2 turn
                if w:
                    break
                player2 = int(input('player2: '))
                if player2 in d and d[player2] != 'X' or 'O':
                    d[player2] = 'O'
                    Turn = False
                    update(d)
                    count += 1
                else:
                    print('invalid move')
                    update(d)

    restart()




