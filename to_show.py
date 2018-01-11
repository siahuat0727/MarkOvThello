from board import Board
from MDP import QLearning
import time
from window import Window

ACTIONS = [i for i in range(12)]
MAX_EPISODES = 1

def rl(table):
    for x in range(MAX_EPISODES):
        board = Board(4)
        window = Window(board)
        color = Board.black
        no_move = 0
        while no_move < 2:
            pos_can_go = board.where_can_go(color)
            if len(pos_can_go) == 0:
                print(color, "no move...")
                no_move += 1
            else:
                print(color, "can move at", end=' ')
                print(pos_can_go)
                no_move = 0
                board.go(pos_can_go[0], color)
            board.print_board()
            color ^= 1
            time.sleep(0.3)
            window.update_all(board)

if __name__ == '__main__':
    table = QLearning(actions=ACTIONS)
    rl(table)
