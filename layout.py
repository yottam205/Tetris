# Game look setting will be coded here
# board looks, tetrominos etc

import random

BOARD_W, BOARD_H = 10, 20

COLORS = [
    (0, 0, 0),      # Empty spaces
    (255,0 ,0),     # Red
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (255, 255, 0)   # Yellow
]

SHAPES = [
    [[1, 1, 1, 1]],     # I
    [[2, 2],            # O
     [2, 2]],
    [[0, 3, 0],         # T
     [3, 3, 3]],
    [[0, 4, 4],      # S shape
     [4, 4, 0]],
    [[5, 5, 0],      # Z shape
     [0, 5, 5]],
    [[6, 0, 0],      # J shape
     [6, 6, 6]],
    [[0, 0, 7],      # L shape
     [7, 7, 7]]
]

def random_shape_color():
    shape_index = random.randint(0, len(SHAPES) - 1)
    random_shape = SHAPES[shape_index]

    color_index = random.randint(1, len(COLORS) -1)
    random_color = COLORS[color_index]

    return random_shape, random_color