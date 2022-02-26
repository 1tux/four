#!/usr/bin/python3.6
import numpy as np
import string

WIDTH = 7
HEIGHT = 6
WIN_CONDITION = 4

INVALID_TURN = -1
FULL_BOARD = -2

class GAME:
    # a widthxheigh array
    # init with zeros -> empty
    # player1 sets 1
    # player2 sets 2
    # winning condition:
    # row
    # column
    # diagonal    
    def __init__(self, width=WIDTH, height=HEIGHT):
        self.width = width
        self.height = height
        self.board = np.zeros((height, width))
        self.turn = 1 # either 1 or 2 for different players

    def is_column_empty(self, col_idx):
        return self.board[0][col_idx] == 0

    def column_to_index(self, column_name):
        try:
            return string.ascii_uppercase.index(column_name[0].upper())
        except:
            return -1

    def do_turn(self, column):
        col_idx = self.column_to_index(column)
        if not (0 <= col_idx < self.width) or not self.is_column_empty(col_idx):
            return INVALID_TURN

        # find place to insert token
        row_i = self.height - 1
        while self.board[row_i][col_idx] != 0:
            row_i -= 1
        self.board[row_i][col_idx] = self.turn

        if self.is_winning():
            return self.turn # the player who won

        if self.is_full():
            return FULL_BOARD
        self.turn = 3 - self.turn # changes turns
        return 0

    def has_winning_row(self, board):
        for i in range(board.shape[0]):
            for j in range(board.shape[1] - WIN_CONDITION + 1):
                # if all [WIN_CONDITION=4] tokens equals the first one
                if board[i][j] != 0 and np.all(board[i][j:j+WIN_CONDITION] == board[i][j]):
                    return True
        return False

    def has_winning_diag(self, board):
        for i in range(board.shape[0] - WIN_CONDITION + 1):
            for j in range(board.shape[1] - WIN_CONDITION + 1):
                sub_board = board[i:i+WIN_CONDITION, j:j+WIN_CONDITION]

                curr = sub_board[0][0]
                if curr != 0 and np.all(np.diag(sub_board) == curr):
                    return True

                curr = np.rot90(sub_board)[0][0]
                if curr != 0 and np.all(np.diag(np.rot90(sub_board)) == curr):
                    return True
        return False

    def is_winning(self):
        # row, column, major diagonals, minor diagonals
        return self.has_winning_row(self.board) or \
        self.has_winning_row(self.board.T) or \
        self.has_winning_diag(self.board)


    def is_full(self):
        for j in range(self.width):
            if self.board[0][j] == 0:
                return False
        return True

    def plot(self):
        print("=" * self.width * 4)
        for i in range(self.height):
            for j in range(self.width):
                print(f"{self.board[i][j]:3.0f}", end=" ")
            print("")
        print("=" * self.width * 4)
        for i in range(self.width):
            print(f"  {string.ascii_uppercase[i]}", end=" ")
        print("")

def main():
    g = GAME()
    while True:
        g.plot()
        col = input(f"Player{g.turn} turn: ")
        res = g.do_turn(col)
        g.plot()
        if res > 0:
            print(f"Player {res} WON!")
            break
        elif res == INVALID_TURN:
            print("Invalid Turn!")
        elif res == FULL_BOARD:
            print("It's a tie!")
            break

if __name__ == "__main__":
    main()