import pygame
import numpy as np
import random
import utils


class SudokuGrid:
    grid = None
    cursorX, cursorY = 0, 0
    grid_width = utils.WINDOW_WIDTH
    grid_height = utils.WINDOW_HEIGHT
    selected_cell = (0, 0)

    def __init__(self):
        pygame.init()
        self.initialize_grid()
        self.grid_surface = pygame.display.set_mode((self.grid_width, self.grid_height))
        # pygame.display.set_caption("Sudoku")

    def initialize_grid(self):
        self.grid = np.zeros((9, 9, 4), dtype=object)
        self.grid[:, :, 1] = {"r": 240, "g": 230, "b": 140}
        self.grid[:, :, 2] = None
        self.grid[:, :, 3] = 55

    def draw_grid(self):
        for x in range(0, utils.WINDOW_WIDTH, utils.CELL_SIZE):
            pygame.draw.line(self.grid_surface, utils.GRAY if x % 3 else utils.BLACK, (x, 0), (x, utils.WINDOW_HEIGHT),
                             2 if x % 3 == 0 else 1)
        for y in range(0, utils.WINDOW_HEIGHT, utils.CELL_SIZE):
            pygame.draw.line(self.grid_surface, utils.GRAY if y % 3 else utils.BLACK, (0, y), (utils.WINDOW_WIDTH, y),
                             2 if y % 3 == 0 else 1)

    def draw_numbers(self):
        def get_cell_color(line, column):
            cell_color = self.grid[line, column, 1]
            # print("cell_color", grid, grid[line, column], cell_color)
            cell_color_tuple = (cell_color["r"], cell_color["g"], cell_color["b"])
            return cell_color_tuple

        for y, row in enumerate(self.grid[:, :, 0]):
            for x, num in enumerate(row):
                if num != 0:
                    pygame.draw.rect(self.grid_surface, get_cell_color(y, x),
                                     (x * utils.CELL_SIZE, y * utils.CELL_SIZE, utils.CELL_SIZE, utils.CELL_SIZE))
                    print("font", self.grid[:, :, 2][y][x])
                    font = pygame.font.Font(self.grid[:, :, 2][y][x], self.grid[:, :, 3][y][x])
                    text = font.render(str(num), 1, (10, 10, 10))
                    text_rect = text.get_rect(
                        center=(x * utils.CELL_SIZE + utils.CELL_SIZE // 2, y * utils.CELL_SIZE + utils.CELL_SIZE // 2))
                    self.grid_surface.blit(text, text_rect)

    def valid(self, row, col, num):
        # Check Row
        for x in range(9):
            if self.grid[row][x] == num:
                return False

        # Check Column
        for x in range(9):
            if self.grid[x][col] == num:
                return False

        # Check Box
        start_row = row - row % 3
        start_col = col - col % 3
        for i in range(3):
            for j in range(3):
                if self.grid[i + start_row][j + start_col] == num:
                    return False

        return True

    def draw_selected_cell(self):
        if self.selected_cell:
            x, y = self.selected_cell
            pygame.draw.rect(self.grid_surface, utils.RED,
                             (x * utils.CELL_SIZE, y * utils.CELL_SIZE, utils.CELL_SIZE, utils.CELL_SIZE), 3)

    def update_display(self):
        self.grid_surface.fill(utils.WHITE)
        self.draw_numbers()
        self.draw_grid()
        self.draw_selected_cell()
        pygame.display.update()

    def solve(self, row=0, col=0):
        if col == 9:
            if row == 8:
                return True
            row += 1
            col = 0

        if self.grid[:, :, 0][row][col] > 0:
            return self.solve(self.grid, row, col + 1)

        for num in range(1, 10):
            if self.valid(self.grid[:, :, 0], row, col, num):
                self.grid[:, :, 0][row][col] = num
                self.grid[:, :, 1][row][col] = {"r": 220, "g": 20, "b": 60}
                # update_display()

                if self.solve(self.grid, row, col + 1):
                    return True

            self.grid[:, :, 0][row][col] = 0
            # update_display()
        print("I'm probably not solvable")
        return False

    def handle_cursor_highlight(self, action):
        if action == "UP":
            self.cursorY = self.cursorY - 1
        elif action == "DOWN":
            self.cursorY = self.cursorY + 1
        elif action == "LEFT":
            self.cursorX = self.cursorX - 1
        elif action == "RIGHT":
            self.cursorX = self.cursorX + 1
        else:
            pass
        if self.cursorX < 0:
            self.cursorX = 0
        if self.cursorY < 0:
            self.cursorY = 0
        if self.cursorX > 8:
            self.cursorX = 8
        if self.cursorY > 8:
            self.cursorY = 8

        self.selected_cell = (self.cursorX, self.cursorY)

    def run(self):
        # initialize_grid()
        clock = pygame.time.Clock()
        # fill_grid()
        # remove_cells()
        run = True
        while run:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                # Detecter le click de la souris et mettre à jour la position du curseur
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.cursorX, self.cursorY = pygame.mouse.get_pos()
                    self.cursorX, self.cursorY = self.cursorX // utils.CELL_SIZE, self.cursorY // utils.CELL_SIZE
                    self.selected_cell = (self.cursorX, self.cursorY)

                if event.type == pygame.KEYDOWN:
                    if event.unicode.isdigit() and 0 < int(event.unicode) <= 9:
                        self.grid[:, :, 0][self.cursorY][self.cursorX] = int(event.unicode)
                        self.grid[:, :, 2][self.cursorY][self.cursorX] = "Kind Handwriting.ttf"

                    elif event.key == pygame.K_RETURN:
                        self.solve()
                    elif event.key == pygame.K_BACKSPACE:
                        self.grid[:, :, 0][self.cursorY][self.cursorX] = 0
                    elif event.key == pygame.K_c:
                        self.grid[:, :, 0] = 0
                    elif event.key == pygame.K_g:
                        self.initialize_grid()
                        self.fill_grid()
                        self.remove_cells()
                    elif event.key == pygame.K_LEFT:
                        self.handle_cursor_highlight("LEFT")
                    elif event.key == pygame.K_RIGHT:
                        self.handle_cursor_highlight("RIGHT")
                    elif event.key == pygame.K_UP:
                        self.handle_cursor_highlight("UP")
                    elif event.key == pygame.K_DOWN:
                        self.handle_cursor_highlight("DOWN")

            self.update_display()
        pygame.quit()

    def is_valid(self, y, x, n):
        """
        Check if number n can be placed at position (y,x)
        """
        if n in self.grid[:, :, 0][y]:  # check row
            return False
        if n in self.grid[:, :, 0][:, x]:  # check column
            return False
        x0 = (x // 3) * 3
        y0 = (y // 3) * 3
        if n in self.grid[:, :, 0][y0:y0 + 3, x0:x0 + 3]:  # check box
            return False
        return True

    def fill_grid(self):
        """
        Fill the Sudoku grid with numbers randomly
        """
        numbers = list(range(1, 10))
        for y in range(9):
            for x in range(9):
                if self.grid[:, :, 0][y][x] == 0:  # If the cell is empty
                    random.shuffle(numbers)  # shuffle numbers before trying
                    for n in numbers:  # For each number from 1-9
                        if self.is_valid(y, x, n):  # If the number can be placed
                            self.grid[:, :, 0][y][x] = n  # Place the number
                            if np.count_nonzero(self.grid[:, :, 0]) == 81 or self.fill_grid():
                                # if grid is full or keep filling if not
                                return True
                            self.grid[:, :, 0][y][x] = 0  # If the number can't be placed, reset cell
                    return False
        return True

    def remove_cells(self):
        """
        Remove numbers from the Sudoku grid randomly
        """
        positions = list(range(81))
        random.shuffle(positions)  # shuffle positions to be removed
        while len(positions) > 21:  # We are going to keep 21 cells filled
            pos = positions.pop()
            y, x = pos // 9, pos % 9
            removed = self.grid[:, :, 0][y][x]
            self.grid[:, :, 0][y][x] = 0

            temp_grid = self.grid.copy()

            if not self.is_solvable(temp_grid):
                self.grid[:, :, 0][y][x] = removed

    def is_solvable(self, solving_grid):
        """
        Check if a Sudoku grid is solvable
        """
        for y in range(9):
            for x in range(9):
                if solving_grid[:, :, 0][y][x] == 0:  # If the cell is empty
                    for n in range(1, 10):  # For each number from 1-9
                        if self.is_valid(y, x, n):  # If the number can be placed
                            solving_grid[:, :, 0][y][x] = n  # Place the number
                            if np.count_nonzero(self.grid[:, :, 0]) == 81 or self.is_solvable(solving_grid):
                                return True
                            solving_grid[:, :, 0][y][x] = 0  # If the number can't be placed, reset cell
                    return False
        return True


class Sudoku:
    
    pass

sudoku = SudokuGrid()
sudoku.run()
