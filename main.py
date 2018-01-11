from board import Board
from MDP import QLearning
import time
import itertools
from window import Window
import numpy as np
import sys

SIZE = 5



mid_r = SIZE//2
mid_l = mid_r - 1
ACTIONS = [(x, y) for x, y in itertools.product(range(SIZE), range(SIZE)) if (x, y) not in [(mid_l, mid_l), (mid_l, mid_r), (mid_r, mid_l), (mid_r, mid_r)]]

def color2str(color):
    return 'black' if color == Board.black else 'white'

def update_board(board, pos_to_go, color):
    if pos_to_go != (-1, -1):
        board.go(pos_to_go, color)
    R = 0
    S_ = board.to_string(color^1)
    if board.game_over():
        winner = board.get_winner()
        if winner == color:
            R = 1
        elif winner == color^1:
            R = -1
        S_ = 'terminal'
    return S_, R

     

            

def rl_no_window(episode):
    table = QLearning(actions=ACTIONS, greedy=0.7)
    board = Board(SIZE)
    for x in range(episode):
        board.board_initialize()
        color = Board.black
        S = board.to_string(color)
        waiting_time = 0 
        while True:
            pos_can_go_s = board.where_can_go(color)
            pos_to_go, pos_can_go_value_s = table.choose_possible_action(S, pos_can_go_s)

            S_, R = update_board(board, pos_to_go, color)
            pos_can_go_s = board.where_can_go(color^1)
            table.othello_learn(S, pos_to_go, R, S_, pos_can_go_s)
            if S_ == 'terminal':
                break
            color ^= 1
            S = S_
        if (x + 1) % 200 == 0:
            board.board_initialize()
            pos_can_go_s = board.where_can_go(board.black)
            color = board.black
            S = board.to_string(color)
            pos_to_go, pos_can_go_value_s = table.choose_possible_action(S, pos_can_go_s)
            # print(table.q_table.sort_index(axis=0))
            print(x+1)
            print(pos_can_go_value_s)
    print(table.q_table.sort_index(axis=0))

def rl(episode):
    table = QLearning(actions=ACTIONS, greedy=0.7)
    board = Board(SIZE)
    window = Window(board)
    for x in range(episode):
        board.board_initialize()
        color = Board.black
        S = board.to_string(color)
        waiting_time = 0 
        while True:
            pos_can_go_s = board.where_can_go(color)
            pos_to_go, pos_can_go_value_s = table.choose_possible_action(S, pos_can_go_s)
            window.update_all(board, wait=waiting_time)
            window.update_all(board, pos_can_go_s, pos_can_go_value_s, wait=waiting_time)

            S_, R = update_board(board, pos_to_go, color)
            pos_can_go_s = board.where_can_go(color^1)
            table.othello_learn(S, pos_to_go, R, S_, pos_can_go_s)
            if S_ == 'terminal':
                window.update_all(board, wait=waiting_time)
                break
            color ^= 1
            S = S_
    board.board_initialize()
    pos_can_go_s = board.where_can_go(board.black)
    color = board.black
    S = board.to_string(color)
    pos_to_go, pos_can_go_value_s = table.choose_possible_action(S, pos_can_go_s)
    # print(table.q_table.sort_index(axis=0))
    # print(pos_can_go_value_s)
    window.update_all(board, pos_can_go_s, pos_can_go_value_s, wait=waiting_time)
    input("already %d"%(x+1))
    print(table.q_table.sort_index(axis=0))

if __name__ == '__main__':
    np.random.seed(2)  # reproducible
    rl_no_window(int(input("How many times to train? ")))
    # table = rl(episode=10)
