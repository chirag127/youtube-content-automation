"""
make a function to make a tic tac toe game
"""
import random


board = [1, 2, 3, 4, 5, 6, 7, 8, 9]
end = False
win_combinations = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))

def draw():
    print(board[0], board[1], board[2])
    print(board[3], board[4], board[5])
    print(board[6], board[7], board[8])
    print()

def choose_number():
    while True:
        try:
            choice = int(input("Please choose a number between 1-9: "))
            if choice in range(1, 10):
                return choice
            else:
                print("Please choose a number between 1-9: ")
        except ValueError:
            print("Please choose a number between 1-9: ")

def p1():
    n = choose_number()
    if board[n] == "X" or board[n] == "O":
        print("\nYou can't go there. Try again")
        p1()
    else:
        board[n] = "X"

def p2():
    n = choose_number()
    if board[n] == "X" or board[n] == "O":
        print("\nYou can't go there. Try again")
        p2()
    else:
        board[n] = "O"

def choose_first():
    flip = random.randint(0, 1)
    if flip == 0:
        return p2
    else:
        return p1

def check_board():
    for i in win_combinations:
        if board[i[0]] == board[i[1]] == board[i[2]] == "X":
            print("Player 1 wins!\n")
            print("Congratulations!\n")
            return True

        if board[i[0]] == board[i[1]] == board[i[2]] == "O":
            print("Player 2 wins!\n")
            print("Congratulations!\n")
            return True
    if " " not in board:
        print("\nThe game ends in a Tie\n")
        return True


def main():
    draw()
    while not end:
        end = check_board()
        if end == True:
            break
        turn = choose_first()
        turn()
        draw()
        end = check_board()


main()
