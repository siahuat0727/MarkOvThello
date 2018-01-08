import numpy as np
import itertools


class Board:
    white = 1
    black = -1
    dir_ = [(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1),(1,0)]

    def __init__(self, size):
        self.size = size
        self.board = np.zeros((size, size), dtype=np.int)
        self.board_initialize()

    def board_initialize(self):
        s = self.size // 2;
        b = s - 1;
        self.board[s][b] = self.board[b][s] = self.white
        self.board[s][s] = self.board[b][b] = self.black
    
    def print_board(self):
        for x in range(self.size):
            for y in range(self.size):
                t = self.board[x][y]
                print(' ' if t == 0 else 'o' if t == self.black else 'x', end=' ')
            print()
    
    def go(self, pos, color, checkOnly):
        x, y = pos
        if x < 0:
            return False
        pos_to_reverse = []
        if self.board[x][y] != 0:
            return False
        can_move = False
        for d in self.dir_:
            x_t, y_t = x, y
            while True:
                x_t, y_t = [sum(i) for i in zip((x_t, y_t), d)]
                # print("in while")
                if not(0 <= x_t < self.size and 0 <= y_t < self.size):
                    break
                if self.board[x_t][y_t] == -color:
                    pos_to_reverse.append((x_t, y_t))
                elif self.board[x_t][y_t] == 0:
                    del pos_to_reverse[:]
                    break
                else: # self.board[x_t][y_t] == color
                    break
            cur_count = len(pos_to_reverse)
            if cur_count != 0:
                can_move = True
                if checkOnly:
                    return True
                for x_tt, y_tt in pos_to_reverse:
                    self.board[x_tt][y_tt] = -self.board[x_tt][y_tt]
        if can_move:
            self.board[x][y] = color
            return True
        return False
    
    def whereCanGo(self, color):
        return [(x, y) for x, y in itertools.product(range(self.size),range(self.size)) if self.go((x, y), color, True)]
    
    def printWhereCanGo(self, color):
        print(whereCanGo(color))

board = Board(6)
board.print_board()
color = Board.black
board.go(board.whereCanGo(color)[0], color, False)
board.print_board()
color = -color

board.go(board.whereCanGo(color)[0], color, False)
board.print_board()
color = -color

board.go(board.whereCanGo(color)[0], color, False)
board.print_board()
color = -color

board.go(board.whereCanGo(color)[0], color, False)
board.print_board()
color = -color
