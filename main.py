from board import Board
from qlearning import MDPTable

ACTIONS = [i for i in range(12)]
MAX_EPISODES = 1

def rl(table):
    for x in range(MAX_EPISODES):
        board = Board(6)
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

if __name__ == '__main__':
    table = MDPTable(actions=ACTIONS)
    rl(table)
