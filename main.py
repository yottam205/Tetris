# main game file where game loop is
# heuristic-based algorithm for self played Tetris game

import pygame
import layout
import random
import time

pygame.init()

CELL_SIZE = 30
WINDOW_W = layout.BOARD_W * CELL_SIZE + 400
WINDOW_H = layout.BOARD_H * CELL_SIZE  + 100
board_start_x = (WINDOW_W - layout.BOARD_W * CELL_SIZE) // 3
board_start_y = (WINDOW_H - layout.BOARD_H * CELL_SIZE) // 2


window = pygame.display.set_mode((WINDOW_W, WINDOW_H))
pygame.display.set_caption("Tetris")
font = pygame.font.SysFont('comicsans', 30)

info_x = board_start_x + layout.BOARD_W * CELL_SIZE + 50
time_y = 30
score_y = 65
lines_y = 100
next_shape_y = 150

button_x = WINDOW_W - 100  # Position button on the far right corner
button_y = WINDOW_H - 70
button_width = 80
button_height = 40

def draw_info(surface, score, start_time, lines):
    current_time = int(time.time() - start_time)
    pygame.draw.rect(surface, (0, 0, 0), (info_x, 0, WINDOW_W - info_x, WINDOW_H))
    # Time
    time_label = font.render(f'Time: {current_time}', 1, (255, 255, 255))
    surface.blit(time_label, (info_x, time_y))
    # Score
    score_label = font.render(f'Score: {score}', 1, (255, 255, 255))
    surface.blit(score_label, (info_x, score_y))
    # Lines cleared
    lines_label = font.render(f'Lines: {lines}', 1, (255, 255, 255))
    surface.blit(lines_label, (info_x, lines_y))

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
    color_index = layout.COLORS.index(tetromino.color)
    for i, row in enumerate(tetromino.shape):
        for j, cell in enumerate(row):
            if cell != 0:
                board_x = tetromino.x + j
                board_y = tetromino.y + i
                if 0 <= board_y < layout.BOARD_H and 0 <= board_x < layout.BOARD_W:
                    game_board[board_y][board_x] = color_index

def check_lines(board):
    lines_cleared = 0
    new_board = [[0 for _ in range(layout.BOARD_W)] for _ in range(layout.BOARD_H)]
    new_row_index = layout.BOARD_H - 1

    for i in range(layout.BOARD_H - 1, -1, -1):
        if 0 not in board[i]:
            lines_cleared += 1
        else:
            new_board[new_row_index] = board[i]
            new_row_index -= 1

    return lines_cleared, new_board



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

# Shadow Tetromino
def draw_shadow_tetromino(surface, tetromino, game_board):
    shadow_color = (200, 200, 200)  # Light grey color for the shadow
    # Create a shadow Tetromino that is a copy of the current one
    shadow = Tetromino(tetromino.shape_index, shadow_color)
    shadow.x, shadow.y = tetromino.x, tetromino.y
    shadow.shape = tetromino.shape

    # Drop shadow to the bottom
    while not is_collision(shadow, game_board):
        shadow.y += 1
    shadow.y -= 1  # Move back up after collision

    for i, row in enumerate(shadow.shape):
        for j, cell in enumerate(row):
            if cell != 0:
                pygame.draw.rect(
                    surface,
                    shadow_color,
                    (board_start_x + (shadow.x + j) * CELL_SIZE,
                     board_start_y + (shadow.y + i) * CELL_SIZE,
                     CELL_SIZE, CELL_SIZE), 
                    2  # Outline width, set to 0 for filled rectangle
                )

    # Draw shadow Tetromino
    draw_tetromino(surface, shadow)

def draw_pause_button(surface, is_paused):
    button_color = (99, 126, 118)  # Dark gray button
    text = "Pause" if not is_paused else "Play"
    text_color = (255, 255, 255)  # White text

    # Draw the button
    pygame.draw.rect(surface, button_color, (button_x, button_y, button_width, button_height))

    # Draw the text
    button_font = pygame.font.SysFont('comicsans', 20)
    text_surface = button_font.render(text, True, text_color)
    surface.blit(text_surface, (button_x + (button_width - text_surface.get_width()) / 2, 
                                button_y + (button_height - text_surface.get_height()) / 2))


# Game Over Screen
def show_game_over(surface):
    game_over_label = font.render('GAME OVER', 1, (255, 0, 0))
    surface.blit(game_over_label, (board_start_x + (layout.BOARD_W * CELL_SIZE // 2) - (game_over_label.get_width() // 2), board_start_y + (layout.BOARD_H * CELL_SIZE // 2) - (game_over_label.get_height() // 2)))
    pygame.display.update()
    pygame.time.wait(3000) 

game_board = [[0 for _ in range(layout.BOARD_W)] for _ in range(layout.BOARD_H)]
current_tetromino = spawn_new_tetromino()
next_tetromino = spawn_new_tetromino()
clock = pygame.time.Clock()
fall_speed = 0.10
lines_cleared = 0
fall_time = 0
running = True
start_time = time.time()  # Start time for the game
score = 0
score_per_tetromino = 10 
is_paused = False


while running:
    fall_time += clock.get_rawtime()
    clock.tick()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                is_paused = not is_paused
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
                fall_speed = 0.03
            elif event.key == pygame.K_SPACE:
                fall_speed = 0.001
            elif event.key == pygame.K_UP:
                current_tetromino.rotate()
                if not valid_space(current_tetromino, game_board):
                    current_tetromino.rotate()  # Rotate back to old state

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN or pygame.K_SPACE:
                fall_speed = 0.10

    if not is_paused:
        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_tetromino.y += 1
            if not valid_space(current_tetromino, game_board) or is_collision(current_tetromino, game_board):
                current_tetromino.y -= 1
                lock_tetromino(current_tetromino, game_board)
                lines_cleared_this_turn, game_board = check_lines(game_board)  # Adjusted to update the board
                lines_cleared += lines_cleared_this_turn
                score += score_per_tetromino
                current_tetromino = next_tetromino
                next_tetromino = spawn_new_tetromino()
                if is_collision(next_tetromino, game_board):
                    show_game_over(window)
                    running = False
        

    window.fill((0, 0, 0))
    draw_grid(window, game_board)
    draw_shadow_tetromino(window, current_tetromino, game_board)
    draw_tetromino(window, current_tetromino)
    draw_next_shape(next_tetromino, window)
    draw_info(window, score, start_time, lines_cleared)
    draw_pause_button(window, is_paused)  # Draw the pause/play button
    pygame.display.update()

    if lines_cleared >= 10:
        fall_speed *= 0.9
        lines_cleared -= 10

    clock.tick(60)

show_game_over(window)
pygame.quit()
