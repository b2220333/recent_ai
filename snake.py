#!/usr/bin/env python3
# encoding: utf-8

import pygame
import random
import sys

# --- 1. 軟體設計：初始化參數 ---
WIDTH, HEIGHT = 600, 400
GRID_SIZE = 20  # 每一格的大小
FPS = 10        # 初始速度，越快越難

# 顏色定義 (RGB)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED   = (255, 0, 0)
BLACK = (0, 0, 0)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("黑客練習：極簡貪食蛇")
    clock = pygame.time.Clock()

    # --- 2. 狀態設計：遊戲變數 ---
    snake = [(100, 100), (80, 100), (60, 100)] # 蛇身座標清單
    direction = pygame.K_RIGHT                  # 初始移動方向
    food = (random.randrange(0, WIDTH, GRID_SIZE), 
            random.randrange(0, HEIGHT, GRID_SIZE))
    score = 0

    while True:
        # A. 事件偵測 (Input)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # 防止蛇「180度直接回頭」自殺
                if event.key == pygame.K_UP and direction != pygame.K_DOWN:
                    direction = event.key
                elif event.key == pygame.K_DOWN and direction != pygame.K_UP:
                    direction = event.key
                elif event.key == pygame.K_LEFT and direction != pygame.K_RIGHT:
                    direction = event.key
                elif event.key == pygame.K_RIGHT and direction != pygame.K_LEFT:
                    direction = event.key

        # B. 邏輯處理 (Logic)
        # 計算新的蛇頭位置
        head_x, head_y = snake[0]
        if direction == pygame.K_UP:    head_y -= GRID_SIZE
        if direction == pygame.K_DOWN:  head_y += GRID_SIZE
        if direction == pygame.K_LEFT:  head_x -= GRID_SIZE
        if direction == pygame.K_RIGHT: head_x += GRID_SIZE
        
        new_head = (head_x, head_y)

        # 碰撞偵測：撞牆或撞到自己
        if (head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT 
            or new_head in snake):
            print(f"Game Over! Your Score: {score}")
            break # 退出迴圈

        snake.insert(0, new_head) # 增加新頭

        # 吃到食物
        if new_head == food:
            score += 1
            food = (random.randrange(0, WIDTH, GRID_SIZE), 
                    random.randrange(0, HEIGHT, GRID_SIZE))
        else:
            snake.pop() # 沒吃到食物，移除蛇尾，維持長度

        # C. 畫面渲染 (Render)
        screen.fill(BLACK)
        # 畫食物
        pygame.draw.rect(screen, RED, (food[0], food[1], GRID_SIZE, GRID_SIZE))
        # 畫蛇
        for segment in snake:
            pygame.draw.rect(screen, GREEN, (segment[0], segment[1], GRID_SIZE, GRID_SIZE))
        
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()


