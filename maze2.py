#!/usr/bin/env python3
# encoding: utf-8

import pygame
import math
import random
import sys

# --- 初始化 ---
WIDTH, HEIGHT = 800, 800
GRID_SIZE = 40
CENTER = (400, 400)
RING_RADIUS = 280
GATE_HITBOX = 75

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("奇門遁甲：伏兵破陣")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Microsoft JhengHei", 20)

# 門與屬性 (1為吉, 0為凶/平)
GATES_INFO = [
    ("開", 1), ("休", 1), ("生", 1), ("傷", 0), 
    ("杜", 0), ("景", 0), ("驚", 0), ("死", 0)
]

# --- 迷宮生成 ---
def generate_maze():
    maze = [[1] * (WIDTH//GRID_SIZE) for _ in range(HEIGHT//GRID_SIZE)]
    # 簡易清空中心與通道邏輯 (略，延用前版)
    for r in range(5, 15):
        for c in range(5, 15): maze[r][c] = 0
    return maze

maze_data = generate_maze()
player_pos = [400.0, 400.0]
steps_taken = 0.0
enemies = []

def spawn_enemy(gx, gy):
    """ 在凶門位置生成伏兵 """
    if len(enemies) < 5: # 限制數量
        enemies.append([gx, gy])

def main_loop():
    global steps_taken, player_pos
    
    while True:
        screen.fill((5, 5, 10))
        active_idx = int(steps_taken) % 8
        
        # 1. 事件處理
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()

        # 2. 玩家移動
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_UP]: dy = -5
        elif keys[pygame.K_DOWN]: dy = 5
        elif keys[pygame.K_LEFT]: dx = -5
        elif keys[pygame.K_RIGHT]: dx = 5

        # 簡單碰撞檢查
        if dx != 0 or dy != 0:
            new_x = player_pos[0] + dx
            new_y = player_pos[1] + dy
            dist = math.hypot(new_x - CENTER[0], new_y - CENTER[1])
            
            # 判斷是否能移動 (簡化邏輯：不在牆內即可)
            if dist < RING_RADIUS + 100:
                player_pos = [new_x, new_y]
                steps_taken += 0.04

        # 3. 伏兵邏輯：每當切換到「凶門」且玩家靠近，生成敵人
        for i, (name, is_lucky) in enumerate(GATES_INFO):
            rad = math.radians(i * 45 - 90)
            gx = CENTER[0] + RING_RADIUS * math.cos(rad)
            gy = CENTER[1] + RING_RADIUS * math.sin(rad)
            
            # 如果是目前的凶門，且玩家靠近，機率觸發伏兵
            if i == active_idx and not is_lucky:
                if math.hypot(player_pos[0]-gx, player_pos[1]-gy) < 100:
                    if random.random() < 0.05: spawn_enemy(gx, gy)

        # 4. 敵人追擊與繪製
        for en in enemies[:]:
            # 向玩家移動
            edx = player_pos[0] - en[0]
            edy = player_pos[1] - en[1]
            dist_en = math.hypot(edx, edy)
            if dist_en > 0:
                en[0] += (edx / dist_en) * 2
                en[1] += (edy / dist_en) * 2
            
            pygame.draw.circle(screen, (255, 0, 0), (int(en[0]), int(en[1])), 8)
            # 觸碰判定
            if dist_en < 15:
                print("陷入死陣！重頭來過")
                player_pos = [400.0, 400.0]
                enemies.clear()

        # 5. 繪製門
        for i, (name, is_lucky) in enumerate(GATES_INFO):
            rad = math.radians(i * 45 - 90)
            gx = CENTER[0] + RING_RADIUS * math.cos(rad)
            gy = CENTER[1] + RING_RADIUS * math.sin(rad)
            
            color = (0, 255, 100) if i == active_idx and is_lucky else (200, 0, 0)
            if i == active_idx:
                pygame.draw.circle(screen, color, (int(gx), int(gy)), GATE_HITBOX, 0 if is_lucky else 2)
            
            txt = font.render(name, True, (255, 255, 255))
            screen.blit(txt, (gx-10, gy-10))

        # 玩家
        pygame.draw.circle(screen, (255, 200, 0), (int(player_pos[0]), int(player_pos[1])), 12)
        
        # 破陣判定
        if math.hypot(player_pos[0]-CENTER[0], player_pos[1]-CENTER[1]) > RING_RADIUS + 50:
            if GATES_INFO[active_idx][1] == 1: # 必須是從吉門出
                print("成功突圍！")
                pygame.quit(); sys.exit()

        pygame.display.flip()
        clock.tick(60)

main_loop()


