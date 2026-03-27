import pygame
import random
import os

WIDTH, HEIGHT = 800, 600
MAP_DATA = [("起點", 0), ("台北", 200), ("機會", 0), ("台中", 250), ("監獄", 0), ("台南", 300), ("命運", 0), ("高雄", 350), ("休息區", 0), ("花蓮", 400), ("機會", 0), ("宜蘭", 450), ("去監獄", 0), ("新竹", 500), ("命運", 0), ("桃園", 550)]

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("按空白鍵或點滑鼠擲骰子")
    clock = pygame.time.Clock()

    # 自動選擇字型
    path = "C:\\Windows\\Fonts\\msjh.ttc"
    font = pygame.font.Font(path, 18) if os.path.exists(path) else pygame.font.SysFont(None, 20)
    
    player_pos = 0
    player_money = 2000
    msg = "請按 空白鍵 或 點擊滑鼠！"

    while True:
        # --- A. 事件偵測 ---
        do_move = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); return
            
            # 偵測空白鍵
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                do_move = True
            
            # 偵測滑鼠點擊 (作為備案)
            if event.type == pygame.MOUSEBUTTONDOWN:
                do_move = True

        # --- B. 邏輯更新 ---
        if do_move:
            dice = random.randint(1, 6)
            player_pos = (player_pos + dice) % len(MAP_DATA)
            player_money -= MAP_DATA[player_pos][1]
            msg = f"擲出 {dice}，來到 {MAP_DATA[player_pos][0]}"
            print(f"DEBUG: 骰子 {dice}, 位置 {player_pos}") # 檢查 CMD 是否有印出

        # --- C. 繪製畫面 ---
        screen.fill((255, 255, 255))
        
        # 繪製地圖
        for i, (name, price) in enumerate(MAP_DATA):
            if i < 5:    x, y = 50 + i*140, 50
            elif i < 9:  x, y = 610, 50 + (i-4)*110
            elif i < 13: x, y = 610 - (i-8)*140, 490
            else:        x, y = 50, 490 - (i-12)*110
            
            pygame.draw.rect(screen, (0,0,0), (x, y, 130, 100), 2)
            screen.blit(font.render(name, True, (0,0,0)), (x+10, y+10))
            if price > 0:
                screen.blit(font.render(f"${price}", True, (0,0,255)), (x+10, y+40))
            
            if i == player_pos:
                pygame.draw.circle(screen, (255,0,0), (x+65, y+75), 15)

        # 顯示 UI
        screen.blit(font.render(f"資產: ${player_money}", True, (200, 150, 0)), (300, 240))
        screen.blit(font.render(msg, True, (0,0,0)), (300, 280))

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()