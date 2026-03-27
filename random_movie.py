#!/usr/bin/env python3
# encoding: utf-8
import pygame
import numpy as np
import time

# 設定參數
WIDTH, HEIGHT = 400, 300
FPS = 30

def main():
    # 初始化 Pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("30 FPS RGB 隨機閃爍 (NumPy 優化)")
    clock = pygame.time.Clock()

    running = True
    while running:
        # 1. 偵測退出事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = True
                pygame.quit()
                return

        # 2. 產生隨機 RGB 矩陣
        # 使用 NumPy 產生 (寬, 高, 3) 的陣列，範圍 0-255
        # dtype=uint8 非常重要，這符合記憶體位元組格式
        random_rgb = np.random.randint(0, 256, (WIDTH, HEIGHT, 3), dtype=np.uint8)

        # 3. 將矩陣渲染到視窗
        # pygame.surfarray 可以直接將 NumPy 矩陣映射到畫面上
        pygame.surfarray.blit_array(screen, random_rgb)

        # 4. 更新畫面並維持 FPS
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()