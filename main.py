import pygame
import sys
from game import Game

# Pygbag兼容代码
import asyncio

async def main():
    # 初始化pygame
    pygame.init()
    
    # 设置窗口大小
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    
    # 创建游戏窗口
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("太空侵略者")
    
    # 创建游戏实例
    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
    
    # 创建时钟对象，用于控制帧率
    clock = pygame.time.Clock()
    
    running = True
    while running:
        # 处理事件
        events = pygame.event.get()
        running = game.handle_events(events)
        
        # 更新游戏状态
        game.update()
        
        # 绘制游戏
        game.draw(screen)
        
        # 控制帧率
        clock.tick(60)
        
        # Pygbag兼容：添加异步等待
        await asyncio.sleep(0)
    
    # 退出游戏
    pygame.quit()

if __name__ == "__main__":
    # Pygbag兼容：使用asyncio.run
    asyncio.run(main())