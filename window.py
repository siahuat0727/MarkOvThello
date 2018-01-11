from tkinter import *
import itertools
import time

class Window(object):
    def __init__(self, board):
        self.root = Tk()
        self.root.geometry('264x324+600+250')
        self.root.title('Toc Project')
        self.btn = [[0 for x in range(board.size)] for x in range(board.size)]
        for x in range(board.size):
            for y in range(board.size):
                self.btn[x][y] = Button(bg='green', width=8, heigh=4, text=str(x) + ' ' + str(y),
                                   command=lambda a=x, b=y: self.btn_chess_click(a, b))
                self.btn[x][y].grid(row=x, column=y)
    
        self.btn_start = Button(width=20, heigh=2, text='START', command=self.btn_start_click)
        self.btn_start.grid(row=7, column=0, columnspan=4)
        self.update_all(board)
        self.root.update()


    def update_all(self, board, pos_can_go_s=[], pos_can_go_value_s=[], wait=0):
        for x, y in itertools.product(range(board.size), range(board.size)):
            disk = board.board[x][y]
            self.change_color(x, y, 'black' if disk == board.black else 'white' if disk == board.white else 'green')
            self.change_text(x, y, '')

        for pos, value in zip(pos_can_go_s, pos_can_go_value_s):
            x, y = pos
            self.change_color(x, y, 'red')
            self.change_text(x, y, str(value))
        self.root.update()
        time.sleep(wait)

    def change_color(self, x=0, y=0, to_state='green'):
        self.btn[x][y]['bg'] = to_state
    
    def change_text(self, x=0, y=0, to_text=''):
        self.btn[x][y]['text'] = to_text[:6]
    
    def btn_chess_click(self, x=0, y=0):
        self.change_color(x, y, 'red')
    
    def btn_start_click(self):
        print('Started!')

