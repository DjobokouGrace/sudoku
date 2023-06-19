import tkinter as tk
import random
import time
from copy import deepcopy
from threading import Thread


class Sudoku:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.board = self.generate_board()

    def generate_board(self):
        base = 3
        side = base * base
        nums = list(range(1, side + 1))
        board = [[nums[(base * (r % base) + r // base + c) % side] for c in range(side)] for r in range(side)]
        rows = [r for g in self.shuffle(range(base)) for r in self.shuffle(range(g * base, (g + 1) * base))]
        cols = [c for g in self.shuffle(range(base)) for c in self.shuffle(range(g * base, (g + 1) * base))]
        board = [[board[r][c] for c in cols] for r in rows]

        squares = side * side
        empties = squares * self.difficulty
        for p in random.sample(range(squares), int(empties)):
            board[p // side][p % side] = 0

        self.start_puzzle = deepcopy(board)
        return board

    def shuffle(self, seq):
        seq = list(seq)
        random.shuffle(seq)
        return seq


class TimerThread(Thread):
    def __init__(self, label):
        Thread.__init__(self)
        self.label = label
        self.start_time = time.time()

    def run(self):
        while True:
            time.sleep(1)
            time_elapsed = time.time() - self.start_time
            minutes, seconds = divmod(time_elapsed, 60)
            time_string = "{:02}:{:02}".format(int(minutes), int(seconds))
            self.label.config(text=time_string)


class SudokuApp:
    def __init__(self, root, difficulty):
        self.root = root
        self.root.geometry("600x600")
        self.sudoku = Sudoku(difficulty)
        self.create_menu_interface()

    def create_menu_interface(self):
        self.play_button = tk.Button(self.root, text='PLAY', command=self.play_game)
        self.quit_button = tk.Button(self.root, text='QUIT', command=self.root.quit)

        self.play_button.pack(side=tk.LEFT)
        self.quit_button.pack(side=tk.RIGHT)

    def play_game(self):
        self.play_button.pack_forget()
        self.quit_button.pack_forget()
        self.create_game_interface()

    def create_game_interface(self):
        self.entries = []
        for i in range(9):
            row_entries = []
            for j in range(9):
                entry = tk.Entry(self.root, width=3)
                entry.grid(row=i, column=j)
                row_entries.append(entry)
                if self.sudoku.board[i][j] != 0:
                    entry.insert(tk.END, str(self.sudoku.board[i][j]))
                    entry.config(state='readonly')
            self.entries.append(row_entries)
        self.check_button = tk.Button(self.root, text='Check', command=self.check_solution)
        self.check_button.grid(row=10, column=0, columnspan=9)

        self.timer_label = tk.Label(self.root)
        self.timer_label.grid(row=11, column=0, columnspan=9)
        timer_thread = TimerThread(self.timer_label)
        timer_thread.start()

    def check_solution(self):
        for i in range(9):
            row = [int(self.entries[i][j].get()) for j in range(9)]
            if not self.is_distinct(row):
                print("Incorrect solution")
                return
        for j in range(9):
            column = [int(self.entries[i][j].get()) for i in range(9)]
            if not self.is_distinct(column):
                print("Incorrect solution")
                return
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                square = [int(self.entries[i + x // 3][j + x % 3].get()) for x in range(9)]
                if not self.is_distinct(square):
                    print("Incorrect solution")
                    return
        print("Correct solution!")

    def is_distinct(self, arr):
        return len(arr) == len(set(arr))


def main():
    root = tk.Tk(className="Sudoku")
    difficulty = 0.10  # Adjust the difficulty here. 0.25 easy, 0.5 medium, 0.75 hard
    SudokuApp(root, difficulty)
    root.mainloop()


if __name__ == '__main__':
    main()
