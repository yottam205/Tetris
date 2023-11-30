# Game look setting will be coded here
# board looks, tetrominos etc

BOARD_W, BOARD_H = 10, 20

COLORS = [
    (0, 0, 0),      # Empty spaces
    (255, 0, 0),    # Red for Shape 1
    (0, 255, 0),    # Green for Shape 2
    (0, 0, 255),    # Blue for Shape 3
    (255, 255, 0),  # Yellow for Shape 4
    (255, 165, 0),  # Orange for Shape 5
    (128, 0, 128),  # Purple for Shape 6
    (0, 255, 255)   # Cyan for Shape 7
]

SHAPES = [
    # I Shape
    [
        [[1, 1, 1, 1]],
        [[1],
         [1],
         [1],
         [1]]
    ],
    # O Shape
    [
        [[2, 2],
         [2, 2]]
    ],
    # T Shape
    [
        [[0, 3, 0],
         [3, 3, 3]],
        [[3, 0],
         [3, 3],
         [3, 0]],
        [[3, 3, 3],
         [0, 3, 0]],
        [[0, 3],
         [3, 3],
         [0, 3]]
    ],
    # S Shape
    [
        [[0, 4, 4],
         [4, 4, 0]],
        [[4, 0],
         [4, 4],
         [0, 4]]
    ],
    # Z Shape
    [
        [[5, 5, 0],
         [0, 5, 5]],
        [[0, 5],
         [5, 5],
         [5, 0]]
    ],
    # J Shape
    [
        [[6, 0, 0],
         [6, 6, 6]],
        [[6, 6],
         [6, 0],
         [6, 0]],
        [[6, 6, 6],
         [0, 0, 6]],
        [[0, 6],
         [0, 6],
         [6, 6]]
    ],
    # L Shape
    [
        [[0, 0, 7],
         [7, 7, 7]],
        [[7, 0],
         [7, 0],
         [7, 7]],
        [[7, 7, 7],
         [7, 0, 0]],
        [[7, 7],
         [0, 7],
         [0, 7]]
    ]
]
