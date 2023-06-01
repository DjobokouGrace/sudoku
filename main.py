import pygame
import numpy as np
import random
import time

# Initialisation de Pygame
pygame.init()

# Dimensions
win_height, win_width = 450, 450
cell_size = win_height // 9
# grid = np.zeros((9,9), dtype=int) # Grid de base
# print(grid)
grid = [
    [5, 3, 4, 0, 0, 0, 9, 1, 2],
    [6, 7, 2, 0, 0, 0, 3, 4, 8],
    [1, 9, 8, 0, 0, 0, 5, 6, 7],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [9, 6, 1, 0, 0, 0, 2, 8, 4],
    [2, 8, 7, 0, 0, 0, 6, 3, 5],
    [3, 4, 5, 0, 0, 0, 1, 7, 9]
]
# grid = [
#     [5, 3, 4, 6, 7, 8, 9, 1, 2],
#     [6, 7, 2, 1, 9, 5, 3, 4, 8],
#     [1, 9, 8, 3, 4, 2, 5, 6, 7],
#     [8, 5, 9, 0, 0, 0, 4, 2, 3],
#     [4, 2, 6, 0, 0, 0, 7, 9, 1],
#     [7, 1, 3, 0, 0, 0, 8, 5, 6],
#     [9, 6, 1, 5, 3, 7, 2, 8, 4],
#     [2, 8, 7, 4, 1, 9, 6, 3, 5],
#     [3, 4, 5, 2, 8, 6, 1, 7, 9]
# ]
# Position initiale du curseur
cursorX, cursorY = 0, 0

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
YELLOW = (240, 230, 140)
RED = (220, 20, 60)

# Créer la fenêtre
window = pygame.display.set_mode((win_width, win_height))


def is_valid(y, x, n):
    """
    Check if number n can be placed at position (y,x)
    """
    global grid
    if n in grid[y]:  # check row
        return False
    if n in grid[:, x]:  # check column
        return False
    x0 = (x // 3) * 3
    y0 = (y // 3) * 3
    if n in grid[y0:y0 + 3, x0:x0 + 3]:  # check box
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
            if grid[y][x] == 0:  # If the cell is empty
                random.shuffle(numbers)  # shuffle numbers before trying
                for n in numbers:  # For each number from 1-9
                    if is_valid(y, x, n):  # If the number can be placed
                        grid[y][x] = n  # Place the number
                        if np.count_nonzero(grid) == 81 or fill_grid():
                            # if grid is full or keep filling if not
                            return True
                        grid[y][x] = 0  # If the number can't be placed, reset cell
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
        removed = grid[y][x]
        grid[y][x] = 0

        temp_grid = grid.copy()

        if not is_solvable(temp_grid):
            grid[y][x] = removed


def is_solvable(grid):
    """
    Check if a Sudoku grid is solvable
    """
    for y in range(9):
        for x in range(9):
            if grid[y][x] == 0:  # If the cell is empty
                for n in range(1, 10):  # For each number from 1-9
                    if is_valid(y, x, n):  # If the number can be placed
                        grid[y][x] = n  # Place the number
                        if np.count_nonzero(grid) == 81 or is_solvable(grid):
                            return True
                        grid[y][x] = 0  # If the number can't be placed, reset cell
                return False
    return True


def draw_grid():
    for x in range(0, win_width, cell_size):
        pygame.draw.line(window, GRAY if x % 3 else BLACK, (x, 0), (x, win_height), 2 if x % 3 == 0 else 1)
    for y in range(0, win_height, cell_size):
        pygame.draw.line(window, GRAY if y % 3 else BLACK, (0, y), (win_width, y), 2 if y % 3 == 0 else 1)


def draw_numbers():
    for y, row in enumerate(grid):
        for x, num in enumerate(row):
            if num != 0:
                pygame.draw.rect(window, YELLOW, (x * cell_size, y * cell_size, cell_size, cell_size))
                font = pygame.font.Font(None, 55)
                text = font.render(str(num), 1, (10, 10, 10))
                text_rect = text.get_rect(center=(x * cell_size + cell_size // 2, y * cell_size + cell_size // 2))
                window.blit(text, text_rect)
                # window.blit(text, (x * cell_size + 15, y * cell_size))


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


selected_cell = None


def draw_selected_cell():
    if selected_cell:
        x, y = selected_cell
        pygame.draw.rect(window, RED, (x * cell_size, y * cell_size, cell_size, cell_size), 3)


def update_display():
    window.fill(WHITE)
    draw_grid()
    draw_numbers()
    draw_selected_cell()
    pygame.display.update()


def solve(grid, row=0, col=0):
    if col == 9:
        if row == 8:
            return True
        row += 1
        col = 0

    if grid[row][col] > 0:
        return solve(grid, row, col + 1)

    for num in range(1, 10):
        if valid(grid, row, col, num):
            grid[row][col] = num
            update_display()

            if solve(grid, row, col + 1):
                return True

        grid[row][col] = 0
        update_display()

    # return False


def main():
    global cursorX, cursorY  # on utilise les variables globales cursorX et cursorY
    global selected_cell
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
                cursorX, cursorY = cursorX // cell_size, cursorY // cell_size
                selected_cell = (cursorX, cursorY)
                # pygame.draw.rect(window, RED, (cursorX * cell_size, cursorY * cell_size, cell_size, cell_size))

            if event.type == pygame.KEYDOWN:
                if event.unicode.isdigit() and 0 < int(event.unicode) <= 9:
                    grid[cursorY][cursorX] = int(event.unicode)

                elif event.key == pygame.K_RETURN:
                    solve(grid)

                elif event.key == pygame.K_BACKSPACE:
                    grid[cursorY][cursorX] = 0

        update_display()

    pygame.quit()


if __name__ == "__main__":
    main()
