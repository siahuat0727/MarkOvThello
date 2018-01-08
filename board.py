import numpy as np
import itertools

class Board:
    black = 0
    white = 1
    empty = 2
    dir_ = [(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1),(1,0)]

    def __init__(self, size):
        self.size = size
        self.board = np.array([2 for x in range(size*size)], dtype=np.int).reshape(size, size)
        self.board_initialize()

    def board_initialize(self):
        s = self.size // 2;
        b = s - 1;
        self.board[s][b] = self.board[b][s] = self.white
        self.board[s][s] = self.board[b][b] = self.black

    def color_to_char(self, color):
        return ' ' if color == self.empty else 'o' if color == self.black else 'x'
    
    def print_board(self):
        print(end='  ')
        for x in range(self.size):
            print(x,end=' ')
        print()
        first_row = [x for x in range(self.size)]
        for x in range(self.size):
            print(x, end=' ')
            for y in range(self.size):
                print(self.color_to_char(self.board[x][y]), end=' ')
            print()
        print()
    
    def go(self, pos, color, checkOnly=False):
        x, y = pos
        if x < 0:
            return False
        pos_to_reverse = []
        if self.board[x][y] != self.empty:
            return False
        can_move = False
        for d in self.dir_:
            x_t, y_t = x, y
            while True:
                x_t, y_t = [sum(i) for i in zip((x_t, y_t), d)]
                # print("in while")
                if not(0 <= x_t < self.size and 0 <= y_t < self.size):
                    break
                if self.board[x_t][y_t] == color^1:
                    pos_to_reverse.append((x_t, y_t))
                elif self.board[x_t][y_t] == self.empty:
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
                    self.board[x_tt][y_tt] ^= 1
        if can_move:
            self.board[x][y] = color
            return True
        return False
    
    def where_can_go(self, color):
        return [(x, y) for x, y in itertools.product(range(self.size),range(self.size)) if self.go((x, y), color, True)]
    
    def can_i_go(self, color):
        return where_can_go(color)

    def print_where_can_go(self, color):
        print(where_can_go(color))
        
    def to_string(self, color):
        return ''.join(str(x) for x in [self.board[x][y] for x, y in itertools.product(range(self.size), range(self.size))]) + str(color)


if __name__ == '__main__':
    board = Board(6)
    board.print_board()
    color = Board.black
    board.go(board.where_can_go(color)[0], color, False)
    board.print_board()
    color = -color
    
    board.go(board.where_can_go(color)[0], color, False)
    board.print_board()
    color = -color
    
    board.go(board.where_can_go(color)[0], color, False)
    board.print_board()
    color = -color
    
    board.go(board.where_can_go(color)[0], color, False)
    board.print_board()
    color = -color
