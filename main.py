# main game file where game loop is
# heuristic-based algorithm for self played Tetris game

import pygame
import layout

pygame.init()

CELL_SIZE = 30
WINDOW_W = layout.BOARD_W * CELL_SIZE
WINDOW_H = layout.BOARD_H * CELL_SIZE

winow = pygame.display.set_mode((WINDOW_W, WINDOW_H))
pygame.display.set_caption("Tetris")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Game logic loop

    pygame.display.update()

pygame.quit()