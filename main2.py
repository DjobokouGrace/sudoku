import pygame
import numpy as np
import random
import time
import utils

# Initialisation de Pygame
pygame.init()


def initialize_grid():
    global grid
    grid = np.zeros((9, 9, 4), dtype=object)
    grid[:, :, 1] = {"r": 240, "g": 230, "b": 140}
    grid[:, :, 2] = None
    grid[:, :, 3] = 55


# Position initiale du curseur
cursorX, cursorY = 0, 0

# Créer la fenêtre
window = pygame.display.set_mode((utils.WINDOW_WIDTH, utils.WINDOW_HEIGHT))
pygame.display.set_caption("Sudoku")


def is_valid(y, x, n):
    """
    Check if number n can be placed at position (y,x)
    """
    global grid
    if n in grid[:, :, 0][y]:  # check row
        return False
    if n in grid[:, :, 0][:, x]:  # check column
        return False
    x0 = (x // 3) * 3
    y0 = (y // 3) * 3
    if n in grid[:, :, 0][y0:y0 + 3, x0:x0 + 3]:  # check box
        return False
    return True


def fill_grid():
    """
    Fill the Sudoku grid with numbers randomly
    """
    global grid
    numbers = list(range(1, 10))
    for y in range(9):
        for x in range(9):
            if grid[:, :, 0][y][x] == 0:  # If the cell is empty
                random.shuffle(numbers)  # shuffle numbers before trying
                for n in numbers:  # For each number from 1-9
                    if is_valid(y, x, n):  # If the number can be placed
                        grid[:, :, 0][y][x] = n  # Place the number
                        if np.count_nonzero(grid[:, :, 0]) == 81 or fill_grid():
                            # if grid is full or keep filling if not
                            return True
                        grid[:, :, 0][y][x] = 0  # If the number can't be placed, reset cell
                return False
    return True


def remove_cells():
    """
    Remove numbers from the Sudoku grid randomly
    """
    global grid
    positions = list(range(81))
    random.shuffle(positions)  # shuffle positions to be removed
    while len(positions) > 21:  # We are going to keep 21 cells filled
        pos = positions.pop()
        y, x = pos // 9, pos % 9
        removed = grid[:, :, 0][y][x]
        grid[:, :, 0][y][x] = 0

        temp_grid = grid.copy()

        if not is_solvable(temp_grid):
            grid[:, :, 0][y][x] = removed


def is_solvable(grid):
    """
    Check if a Sudoku grid is solvable
    """

    for y in range(9):
        for x in range(9):
            if grid[:, :, 0][y][x] == 0:  # If the cell is empty
                for n in range(1, 10):  # For each number from 1-9
                    if is_valid(y, x, n):  # If the number can be placed
                        grid[:, :, 0][y][x] = n  # Place the number
                        if np.count_nonzero(grid[:, :, 0]) == 81 or is_solvable(grid):
                            return True
                        grid[:, :, 0][y][x] = 0  # If the number can't be placed, reset cell
                return False
    return True


def draw_grid():
    for x in range(0, utils.WINDOW_WIDTH, utils.CELL_SIZE):
        pygame.draw.line(window, utils.GRAY if x % 3 else utils.BLACK, (x, 0), (x, utils.WINDOW_HEIGHT),
                         2 if x % 3 == 0 else 1)
    for y in range(0, utils.WINDOW_HEIGHT, utils.CELL_SIZE):
        pygame.draw.line(window, utils.GRAY if y % 3 else utils.BLACK, (0, y), (utils.WINDOW_WIDTH, y),
                         2 if y % 3 == 0 else 1)


def draw_numbers():
    def get_cell_color(line, column):
        cell_color = grid[line, column, 1]
        #print("cell_color", grid, grid[line, column], cell_color)
        cell_color_tuple = (cell_color["r"], cell_color["g"], cell_color["b"])
        return cell_color_tuple

    for y, row in enumerate(grid[:, :, 0]):
        for x, num in enumerate(row):
            if num != 0:
                pygame.draw.rect(window, get_cell_color(y, x),
                                 (x * utils.CELL_SIZE, y * utils.CELL_SIZE, utils.CELL_SIZE, utils.CELL_SIZE))
                font = pygame.font.Font(grid[:, :, 2][y][x], grid[:, :, 3][y][x])
                text = font.render(str(num), 1, (10, 10, 10))
                text_rect = text.get_rect(
                    center=(x * utils.CELL_SIZE + utils.CELL_SIZE // 2, y * utils.CELL_SIZE + utils.CELL_SIZE // 2))
                window.blit(text, text_rect)


def valid(grid, row, col, num):
    # Check Row
    for x in range(9):
        if grid[row][x] == num:
            return False

    # Check Column
    for x in range(9):
        if grid[x][col] == num:
            return False

    # Check Box
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if grid[i + start_row][j + start_col] == num:
                return False

    return True


def draw_selected_cell():
    if selected_cell:
        x, y = selected_cell
        pygame.draw.rect(window, utils.RED,
                         (x * utils.CELL_SIZE, y * utils.CELL_SIZE, utils.CELL_SIZE, utils.CELL_SIZE), 3)


def update_display():
    window.fill(utils.WHITE)
    draw_numbers()
    draw_grid()
    draw_selected_cell()
    pygame.display.update()


def solve(grid, row=0, col=0):
    if col == 9:
        if row == 8:
            return True
        row += 1
        col = 0

    if grid[:, :, 0][row][col] > 0:
        return solve(grid, row, col + 1)

    for num in range(1, 10):
        if valid(grid[:, :, 0], row, col, num):
            grid[:, :, 0][row][col] = num
            grid[:, :, 1][row][col] = {"r": 220, "g": 20, "b": 60}
            # update_display()

            if solve(grid, row, col + 1):
                return True

        grid[:, :, 0][row][col] = 0
        # update_display()
    print("I'm probably not solvable")
    return False


def handle_cursor_highlight(action):
    global cursorX, cursorY
    global selected_cell

    if action == "UP":
        cursorY = cursorY - 1
    elif action == "DOWN":
        cursorY = cursorY + 1
    elif action == "LEFT":
        cursorX = cursorX - 1
    elif action == "RIGHT":
        cursorX = cursorX + 1
    else:
        pass
    if cursorX < 0:
        cursorX = 0
    if cursorY < 0:
        cursorY = 0
    if cursorX > 8:
        cursorX = 8
    if cursorY > 8:
        cursorY = 8

    selected_cell = (cursorX, cursorY)



def main():
    global cursorX, cursorY  # on utilise les variables globales cursorX et cursorY
    global selected_cell
    selected_cell = None
    initialize_grid()
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
                cursorX, cursorY = pygame.mouse.get_pos()
                cursorX, cursorY = cursorX // utils.CELL_SIZE, cursorY // utils.CELL_SIZE
                selected_cell = (cursorX, cursorY)

            if event.type == pygame.KEYDOWN:
                if event.unicode.isdigit() and 0 < int(event.unicode) <= 9:
                    grid[:, :, 0][cursorY][cursorX] = int(event.unicode)
                    grid[:, :, 2][cursorY][cursorX] = "Kind Handwriting.ttf"

                elif event.key == pygame.K_RETURN:
                    solve(grid)
                elif event.key == pygame.K_BACKSPACE:
                    grid[:, :, 0][cursorY][cursorX] = 0
                elif event.key == pygame.K_c:
                    grid[:, :, 0] = 0
                elif event.key == pygame.K_g:
                    initialize_grid()
                    fill_grid()
                    remove_cells()
                elif event.key == pygame.K_LEFT:
                    handle_cursor_highlight("LEFT")
                elif event.key == pygame.K_RIGHT:
                    handle_cursor_highlight("RIGHT")
                elif event.key == pygame.K_UP:
                    handle_cursor_highlight("UP")
                elif event.key == pygame.K_DOWN:
                    handle_cursor_highlight("DOWN")

        update_display()

    pygame.quit()


if __name__ == "__main__":
    main()
