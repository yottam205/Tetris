# main game file where game loop is
# heuristic-based algorithm for self played Tetris game

import pygame
import layout
import random

pygame.init()

CELL_SIZE = 30
WINDOW_W = layout.BOARD_W * CELL_SIZE + 100
WINDOW_H = layout.BOARD_H * CELL_SIZE  + 100
board_start_x = (WINDOW_W - layout.BOARD_W * CELL_SIZE) // 2
board_start_y = (WINDOW_H - layout.BOARD_H * CELL_SIZE) // 2


window = pygame.display.set_mode((WINDOW_W, WINDOW_H))
pygame.display.set_caption("Tetris")

def draw_grid(surface, grid):
    for i in range(layout.BOARD_H):
        for j in range(layout.BOARD_W):
            color_index = grid[i][j]
            color = layout.COLORS[color_index]
            pygame.draw.rect(surface, color,
                             (board_start_x + j * CELL_SIZE, board_start_y + i * CELL_SIZE, CELL_SIZE, CELL_SIZE), 0)                    
            pygame.draw.rect(surface, (128, 128, 128), 
                             (board_start_x + j * CELL_SIZE, board_start_y + i * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)



class Tetromino:
    def __init__(self, shape_index, color):
        self.shape_index = shape_index
        self.all_rotations = layout.SHAPES[shape_index]
        self.rotation = 0
        self.shape = self.all_rotations[self.rotation]
        self.color = color
        self.x = int(layout.BOARD_W / 2) - int(len(self.shape[0]) / 2)
        self.y = 0

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.all_rotations)
        self.shape = self.all_rotations[self.rotation]


def draw_tetromino(surface, tetromino):
    for i, row in enumerate(tetromino.shape):
        for j, cell in enumerate(row):
            if cell != 0:
                pygame.draw.rect(
                    surface,
                    tetromino.color,
                    (board_start_x + (tetromino.x + j) * CELL_SIZE,
                     board_start_y + (tetromino.y + i) * CELL_SIZE,
                     CELL_SIZE, CELL_SIZE),
                    0
                )


def is_collision(tetromino, game_board):
    for i, row in enumerate(tetromino.shape):
        for j, cell in enumerate(row):
            if cell != 0:
                if (tetromino.x + j < 0 or
                    tetromino.x + j >= layout.BOARD_W or
                    tetromino.y + i >= layout.BOARD_H or
                    game_board[tetromino.y + i][tetromino.x + j] != 0):
                    return True
    return False

def lock_tetromino(tetromino, game_board):
    # Find the index of the tetromino's color in the COLORS array
    color_index = layout.COLORS.index(tetromino.color)
    for i, row in enumerate(tetromino.shape):
        for j, cell in enumerate(row):
            if cell != 0:
                board_x = tetromino.x + j
                board_y = tetromino.y + i
                if 0 <= board_y < layout.BOARD_H and 0 <= board_x < layout.BOARD_W:
                    # Store the color index, not the color itself
                    game_board[board_y][board_x] = color_index


def check_lines(board):
    lines_cleared = 0
    for i in range(len(board) - 1, -1, -1):
        if 0 not in board[i]:
            del board[i]
            board.insert(0, [0 for _ in range(layout.BOARD_W)])
            lines_cleared += 1
    return lines_cleared

def valid_space(tetromino, grid):
    accepted_positions = [[(j, i) for j in range(layout.BOARD_W) if grid[i][j] == 0] for i in range(layout.BOARD_H)]
    accepted_positions = [j for sub in accepted_positions for j in sub]

    formatted = convert_shape_format(tetromino)

    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
    return True

def convert_shape_format(tetromino):
    positions = []
    for i, line in enumerate(tetromino.shape):
        for j, cell in enumerate(line):
            if cell != 0:
                positions.append((tetromino.x + j, tetromino.y + i))
    return positions

def draw_next_shape(shape, surface):
    offset_x = board_start_x + layout.BOARD_W * CELL_SIZE + 50  # Display next to the board
    offset_y = board_start_y + 50  # Align vertically with the board

    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, (255, 255, 255))
    surface.blit(label, (offset_x, offset_y - 30))  # Adjust label position as needed

    for i, row in enumerate(shape.shape):
        for j, cell in enumerate(row):
            if cell != 0:
                pygame.draw.rect(surface, shape.color, 
                                 (offset_x + j * CELL_SIZE, 
                                  offset_y + i * CELL_SIZE, 
                                  CELL_SIZE, CELL_SIZE), 0)


def spawn_new_tetromino():
    shape_index = random.randint(0, len(layout.SHAPES) - 1)
    color = layout.COLORS[shape_index + 1]  # +1 to skip the empty space color
    return Tetromino(shape_index, color)




game_board = [[0 for _ in range(layout.BOARD_W)] for _ in range(layout.BOARD_H)]
current_tetromino = spawn_new_tetromino()
clock = pygame.time.Clock()
fall_speed = 0.13
lines_cleared = 0
fall_time = 0
running = True

# Initialize the next tetromino at the start
next_tetromino = spawn_new_tetromino()

while running:
    fall_time += clock.get_rawtime()
    clock.tick()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                current_tetromino.x -= 1
                if not valid_space(current_tetromino, game_board):
                    current_tetromino.x += 1
            elif event.key == pygame.K_RIGHT:
                current_tetromino.x += 1
                if not valid_space(current_tetromino, game_board):
                    current_tetromino.x -= 1
            elif event.key == pygame.K_DOWN:
                fall_speed = 0.05
            elif event.key == pygame.K_UP:
                current_tetromino.rotate()
                if not valid_space(current_tetromino, game_board):
                    current_tetromino.rotate()  # Rotate back to old state

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                fall_speed = 0.13

    if is_collision(current_tetromino, game_board):
        current_tetromino.y -= 1
        lock_tetromino(current_tetromino, game_board)

    if fall_time/1000 > fall_speed:
        fall_time = 0
        current_tetromino.y += 1
        if not valid_space(current_tetromino, game_board):
            current_tetromino.y -= 1
            lock_tetromino(current_tetromino, game_board)  # Lock the tetromino
            current_tetromino = next_tetromino
            next_tetromino = spawn_new_tetromino()
            if next_tetromino is None:
                print("Game Over")
                running = False

    window.fill((0, 0, 0))
    draw_grid(window, game_board)
    draw_tetromino(window, current_tetromino)
    draw_next_shape(next_tetromino, window)
    pygame.display.update()

    if lines_cleared >= 10:
        fall_speed *= 0.9
        lines_cleared -= 10

    clock.tick(60)

pygame.quit()
