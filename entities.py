import pygame
import random
import numpy as np

class Player:
    def __init__(self, x, y, width=50, height=50):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = 5
        self.lives = 3
        self.score = 0
        self.color = (0, 128, 255)
        self.rect = pygame.Rect(x, y, width, height)
        self.shoot_delay = 200  # 射击延迟（毫秒）
        self.last_shot = pygame.time.get_ticks()
    
    def update(self, keys, screen_width):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.velocity
        if keys[pygame.K_RIGHT] and self.x < screen_width - self.width:
            self.x += self.velocity
        self.rect.x = self.x
        self.rect.y = self.y
    
    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.shoot_delay:
            self.last_shot = current_time
            return Bullet(self.x + self.width // 2 - 2, self.y - 10, -8)
        return None
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        # 绘制玩家飞船细节
        pygame.draw.rect(screen, (255, 255, 255), (self.x + 15, self.y, 20, 10))
        pygame.draw.polygon(screen, (255, 255, 255), [(self.x + 25, self.y - 10), (self.x, self.y), (self.x + 50, self.y)])

class Enemy:
    def __init__(self, x, y, enemy_type=1):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.velocity = 1
        self.direction = 1  # 1: 右, -1: 左
        self.enemy_type = enemy_type
        self.color = self.get_color()
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.shoot_delay = random.randint(500, 2000)  # 射击延迟
        self.last_shot = pygame.time.get_ticks()
        self.points = self.get_points()
    
    def get_color(self):
        colors = [(255, 0, 0), (0, 255, 0), (255, 255, 0)]
        return colors[self.enemy_type - 1]
    
    def get_points(self):
        points = [10, 20, 30]
        return points[self.enemy_type - 1]
    
    def update(self):
        self.x += self.velocity * self.direction
        self.rect.x = self.x
        self.rect.y = self.y
    
    def change_direction(self):
        self.direction *= -1
        self.y += 20  # 向下移动
    
    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.shoot_delay:
            self.last_shot = current_time
            return Bullet(self.x + self.width // 2 - 2, self.y + self.height, 5)
        return None
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        # 绘制敌人细节
        pygame.draw.rect(screen, (255, 255, 255), (self.x + 10, self.y + 10, 20, 5))
        pygame.draw.rect(screen, (255, 255, 255), (self.x + 10, self.y + 25, 20, 5))

class Bullet:
    def __init__(self, x, y, velocity):
        self.x = x
        self.y = y
        self.width = 4
        self.height = 10
        self.velocity = velocity
        self.color = (255, 255, 255)
        self.rect = pygame.Rect(x, y, self.width, self.height)
    
    def update(self):
        self.y += self.velocity
        self.rect.y = self.y
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 10
        self.max_size = 50
        self.growth_rate = 2
        self.alpha = 255
        self.fade_rate = 5
        self.active = True
    
    def update(self):
        if self.size < self.max_size:
            self.size += self.growth_rate
        self.alpha -= self.fade_rate
        if self.alpha <= 0:
            self.active = False
    
    def draw(self, screen):
        if self.active:
            surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            pygame.draw.circle(surf, (255, 255, 0, self.alpha), (self.size, self.size), self.size)
            screen.blit(surf, (self.x - self.size, self.y - self.size))

class PowerUp:
    def __init__(self, x, y, power_type):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.velocity = 2
        self.power_type = power_type
        self.color = self.get_color()
        self.rect = pygame.Rect(x, y, self.width, self.height)
    
    def get_color(self):
        colors = [(0, 255, 255), (255, 0, 255), (255, 255, 0)]
        return colors[self.power_type]
    
    def update(self):
        self.y += self.velocity
        self.rect.y = self.y
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        # 绘制电源图标
        if self.power_type == 0:  # 速度提升
            pygame.draw.line(screen, (255, 255, 255), (self.x + 5, self.y + 15), (self.x + 25, self.y + 15), 3)
        elif self.power_type == 1:  # 生命恢复
            pygame.draw.circle(screen, (255, 255, 255), (self.x + 15, self.y + 15), 8)
        elif self.power_type == 2:  # 火力增强
            pygame.draw.line(screen, (255, 255, 255), (self.x + 15, self.y + 5), (self.x + 15, self.y + 25), 3)
            pygame.draw.line(screen, (255, 255, 255), (self.x + 5, self.y + 15), (self.x + 25, self.y + 15), 3)