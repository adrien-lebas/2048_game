import random
import numpy as np
import math
from random import randint
import time
import pandas as pd

def add_number_in_board(board) :
    print("--> adding a number to board")
    result =""
    test = False
    count = 0
    while test == False and count < 120 :
        random1 = randint(0, 3)
        random2 = randint(0, 3)
        value = board[random1][random2]
        if value == 0 :
            test = True
        count += 1
    nums = [2,4]
    random3 = np.random.choice(nums)
    board[random1][random2] = random3
    string = "--> random "+str(random3)+" was added in position : "+str(random1)+":"+str(random2)
    print(string)
    return(board)

def update_board(board,update_score=1):
    print("  --> updating board")
    global score
    for i in range(0,len(board)) :
        for j in range(0,len(board[i])) :
            k = 1
            while j+k < len(board[i]) :
                if board[i][j] != 0 and board[i][j] == board[i][j+k] :
                    if update_score == 1 :
                        score += math.log(board[i][j],2) * board[i][j] * 2
                    board[i][j] *= 2
                    board[i][j+k] = 0
                    break
                elif board[i][j+k] != 0 :
                    break
                k += 1
        for j in range(0,len(board[i])) :
            k = 1
            if board[i][j] != 0 :
                k = 1
                while j - k >= 0 :
                    if board[i][j-k] == 0 :
                        board[i][j-k] = board[i][j-k+1]
                        board[i][j-k+1] = 0
                    k += 1
    print(board)
    return(board)

def first_rotate_board(board,input_player):
    print("  --> first rotating board")
    if input_player == "R" :
        board = np.rot90(np.rot90(board))
    if input_player == "U" :
        board = np.rot90(board)
    if input_player == "D" :
        board = np.rot90(np.rot90(np.rot90(board)))
    print(board)
    return(board)

def second_rotate_board(board,input_player):
    print("  --> second rotating board")
    if input_player == "R" :
        board = np.rot90(np.rot90(board))
    if input_player == "D" :
        board = np.rot90(board)
    if input_player == "U" :
        board = np.rot90(np.rot90(np.rot90(board)))
    print(board)
    return(board)

def test_move(board,move) :
    print("--> testing move "+str(move)+" in board")
    result = False
    board1 = np.save('board1', board)
    board2 = first_rotate_board(board,move)
    board3 = update_board(board2,0)
    board4 = second_rotate_board(board3,move)
    board5 = np.load('board1.npy')
    for i in range(0,len(board)) :
        for j in range(len(board)) :
            if board4[i][j] != board5[i][j] :
                result = True
    print("--> result for move "+str(move)+" in board : "+str(result))
    return(result)

def turn(board,nb) :
    print("--> turn " + str(nb))
    board = add_number_in_board(board)
    print(board)
    theoric_list = ["L","R","U","D"]
    actual_list = []
    np.save('board', board)
    for i in theoric_list :
        board_to_test = np.load('board.npy')
        if test_move(board_to_test,i) :
            actual_list.append(i)
    while True:
        if actual_list == []:
            print("No possible move")
            raise Exception("Pas de coup possible")
        try:
            print("--> list of possible move : " + str(actual_list))
            ia_move(board,actual_list)
            #input_player = raw_input("your move : L/R/U/D --> ")
            input_player = random.choice(actual_list)
            print("--> move choice : "+str(input_player))
        except :
            print("Sorry, I didn't understand that.")
            break
        if input_player not in ["L","R","U","D"]:
            print("Sorry, your response must be L, R, U or D.")
            continue
        else:
            break
    board = np.load('board.npy')
    board = first_rotate_board(board,input_player)
    board = update_board(board)
    board = second_rotate_board(board,input_player)
    np.save('board', board)
    print(board)
    return(board)

def ia_move(board,actual_list) :
    print("--> IA search best move")
    result = pd.DataFrame(["move","board_max"])
    np.save('board2', board)
    board1 = board
    print(board1)
    for i in actual_list :
        board1 = np.load('board2.npy')
        print("--> IA test move : "+i)
        board2 = first_rotate_board(board1,i)
        board3 = update_board(board2,0)
        board4 = second_rotate_board(board3,i)
        board5 = np.load('board2.npy')
        board_max = np.amax(board4)
        result = result.append([{"move":i,"board_max":board_max}])
        print("--> result for move "+str(i)+" in board : "+str(board_max))
    print(result)
            
def game():
    global score    
    board = np.array([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])
    nb = 0
    score = 0
    while True :
        try :
            print("\nNEW TURN\n")
            print("--> score : "+str(score))
            board = turn(board,nb)
            nb += 1
        except :
            print(ValueError)
            print("Sorry, you lose")
            print("nb of turn : "+str(nb))
            print("score : "+str(score))
            time.sleep(2)
            nb = 0
            board = np.array([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])
            score = 0
            continue
    print("you lose")
game()

