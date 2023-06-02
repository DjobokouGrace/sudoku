# Dimensions
WINDOW_HEIGHT = 450
WINDOW_WIDTH = 450

CELL_SIZE = WINDOW_HEIGHT // 9

# Custom grids
CUSTOM_GRID_ONE = [
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

CUSTOM_GRID_TWO = [
    [5, 3, 4, 6, 7, 8, 9, 1, 2],
    [6, 7, 2, 1, 9, 5, 3, 4, 8],
    [1, 9, 8, 3, 4, 2, 5, 6, 7],
    [8, 5, 9, 0, 0, 0, 4, 2, 3],
    [4, 2, 6, 0, 0, 0, 7, 9, 1],
    [7, 1, 3, 0, 0, 0, 8, 5, 6],
    [9, 6, 1, 5, 3, 7, 2, 8, 4],
    [2, 8, 7, 4, 1, 9, 6, 3, 5],
    [3, 4, 5, 2, 8, 6, 1, 7, 9]
]

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
YELLOW = (240, 230, 140)
RED = (220, 20, 60)

# Cell params
CELL_DEFAULT = [
    YELLOW,
    None,
    55
]
CELL_USER_TYPED = [
    YELLOW,
    "Kind Handwriting.ttf",
    55
]
CELL_SYSTEM_SOLVED = [
    RED,
    "Kind Handwriting.ttf",
    55
]