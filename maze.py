#!/usr/bin/env python3
# encoding: utf-8

import pygame
import math

# --- 基礎設定 ---
pygame.init()
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("奇門遁甲：動態迷宮")
clock = pygame.time.Clock()

# 顏色
BLACK = (20, 20, 20)
WHITE = (255, 255, 255)
PLAYER_COLOR = (0, 150, 255)
OPEN_COLOR = (0, 255, 100)    # 吉門
CLOSED_COLOR = (255, 50, 50)  # 凶門

# 八門數據
GATES_NAMES = ["開", "休", "生", "傷", "杜", "景", "驚", "死"]
CENTER = (WIDTH // 2, HEIGHT // 2)
RADIUS = 250
GATE_RADIUS = 40

class Player:
    def __init__(self):
        self.pos = list(CENTER)
        self.speed = 5
        self.size = 15

    def move(self, keys):
        new_pos = self.pos[:]
        if keys[pygame.K_UP]:    new_pos[1] -= self.speed
        if keys[pygame.K_DOWN]:  new_pos[1] += self.speed
        if keys[pygame.K_LEFT]:  new_pos[0] -= self.speed
        if keys[pygame.K_RIGHT]: new_pos[0] += self.speed
        return new_pos

def main():
    player = Player()
    font = pygame.font.SysFont("Microsoft JhengHei", 28)
    running = True

    while running:
        screen.fill(BLACK)
        ticks = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()

        # 1. 計算八門當前狀態 (隨時間轉動)
        # 每 1.5 秒換一次主導門
        active_gate_idx = (ticks // 1500) % 8
        
        # 2. 處理玩家移動與碰撞
        next_pos = player.move(keys)
        can_move = True

        # 繪製與碰撞判定邏輯
        gate_rects = []
        for i, name in enumerate(GATES_NAMES):
            angle = math.radians(i * 45 - 90)
            gx = CENTER[0] + RADIUS * math.cos(angle)
            gy = CENTER[1] + RADIUS * math.sin(angle)
            
            # 判斷門是否開啟 (目前邏輯：主導門及左右相鄰開啟)
            is_open = (i == active_gate_idx or i == (active_gate_idx+1)%8 or i == (active_gate_idx-1)%8)
            
            # 碰撞檢查：如果門是關閉的，玩家不能進入其半徑內
            dist = math.hypot(next_pos[0] - gx, next_pos[1] - gy)
            if not is_open and dist < (GATE_RADIUS + player.size):
                can_move = False # 撞到關閉的門
            
            # 繪製門
            color = OPEN_COLOR if is_open else CLOSED_COLOR
            width = 0 if is_open else 3 # 開門為實心，關門為空心
            pygame.draw.circle(screen, color, (int(gx), int(gy)), GATE_RADIUS, width)
            
            # 繪製文字
            txt = font.render(name, True, WHITE)
            screen.blit(txt, (gx - 15, gy - 15))

        # 更新位置
        if can_move:
            player.pos = next_pos

        # 3. 繪製玩家
        pygame.draw.rect(screen, PLAYER_COLOR, (player.pos[0]-10, player.pos[1]-10, 20, 20))

        # 4. 事件處理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 說明文字
        instruction = font.render("避開紅門(凶)，從綠門(吉)穿出邊界即勝利", True, WHITE)
        screen.blit(instruction, (20, 20))

        # 勝負判定：逃出圓陣
        if math.hypot(player.pos[0]-CENTER[0], player.pos[1]-CENTER[1]) > RADIUS + 60:
            print("成功破陣！")
            running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()


