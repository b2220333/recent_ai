#!/usr/bin/env python3
# encoding: utf-8

import pygame
import random

# --- 1. 軟體設計：常數定義 ---
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 500
BLOCK_SIZE = 30
COLUMNS, ROWS = 10, 15
# 計算遊戲區域左上角偏移量，讓畫面置中
X_OFFSET = (SCREEN_WIDTH - COLUMNS * BLOCK_SIZE) // 2
Y_OFFSET = SCREEN_HEIGHT - ROWS * BLOCK_SIZE - 20

# 七種方塊形狀 (座標定義)
SHAPES = [
    [[1, 1, 1, 1]], # I
    [[1, 1], [1, 1]], # O
    [[0, 1, 0], [1, 1, 1]], # T
    [[0, 1, 1], [1, 1, 0]], # S
    [[1, 1, 0], [0, 1, 1]], # Z
    [[1, 0, 0], [1, 1, 1]], # J
    [[0, 0, 1], [1, 1, 1]]  # L
]
COLORS = [(0,255,255), (255,255,0), (128,0,128), (0,255,0), (255,0,0), (0,0,255), (255,165,0)]

class Piece:
    def __init__(self, x, y, shape):
        self.x, self.y = x, y
        self.shape = shape
        self.color = COLORS[SHAPES.index(shape)]
        self.rotation = 0

def create_grid(locked_pos):
    grid = [[(0,0,0) for _ in range(COLUMNS)] for _ in range(ROWS)]
    for (x, y), color in locked_pos.items():
        if y >= 0: grid[y][x] = color
    return grid

def convert_shape_format(piece):
    positions = []
    shape = piece.shape
    for i, row in enumerate(shape):
        for j, column in enumerate(row):
            if column == 1:
                positions.append((piece.x + j, piece.y + i))
    return positions

def valid_space(piece, grid):
    accepted_pos = [[(j, i) for j in range(COLUMNS) if grid[i][j] == (0,0,0)] for i in range(ROWS)]
    accepted_pos = [j for sub in accepted_pos for j in sub]
    formatted = convert_shape_format(piece)
    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1: return False
    return True

def clear_rows(grid, locked):
    inc = 0
    for i in range(len(grid)-1, -1, -1):
        if (0,0,0) not in grid[i]:
            inc += 1
            locked_pos_row(locked, i)
            shift_rows_down(locked, i)
    return inc

def locked_pos_row(locked, row):
    for (x, y) in list(locked.keys()):
        if y == row: del locked[(x, y)]

def shift_rows_down(locked, row):
    for (x, y) in sorted(list(locked.keys()), key=lambda x: x[1])[::-1]:
        if y < row:
            color = locked.pop((x, y))
            locked[(x, y + 1)] = color

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    locked_positions = {}
    current_piece = Piece(5, 0, random.choice(SHAPES))
    fall_time = 0
    
    while True:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        # 自動下落邏輯
        if fall_time/1000 > 0.5:
            current_piece.y += 1
            if not valid_space(current_piece, grid):
                current_piece.y -= 1
                for pos in convert_shape_format(current_piece):
                    locked_positions[pos] = current_piece.color
                current_piece = Piece(5, 0, random.choice(SHAPES))
                clear_rows(grid, locked_positions)
            fall_time = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid): current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid): current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid): current_piece.y -= 1
                if event.key == pygame.K_UP: # 旋轉邏輯：矩陣轉置 + 翻轉
                    old_shape = current_piece.shape
                    current_piece.shape = [list(row) for row in zip(*current_piece.shape[::-1])]
                    if not valid_space(current_piece, grid): current_piece.shape = old_shape

        screen.fill((40, 40, 40))
        # 畫格子
        for i in range(ROWS):
            for j in range(COLUMNS):
                pygame.draw.rect(screen, grid[i][j], (X_OFFSET + j*BLOCK_SIZE, Y_OFFSET + i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
        
        # 畫當前方塊
        for x, y in convert_shape_format(current_piece):
            if y >= 0:
                pygame.draw.rect(screen, current_piece.color, (X_OFFSET + x*BLOCK_SIZE, Y_OFFSET + y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

        pygame.display.update()

if __name__ == "__main__": main()


