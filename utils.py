import pygame
import os
import platform

def load_sound(filename):
    """加载音效文件"""
    try:
        sound_path = os.path.join('assets', 'sounds', filename)
        return pygame.mixer.Sound(sound_path)
    except:
        return None

def load_image(filename):
    """加载图像文件"""
    try:
        image_path = os.path.join('assets', 'images', filename)
        return pygame.image.load(image_path)
    except:
        return None

def draw_text(surface, text, font, color, x, y):
    """在屏幕上绘制文本"""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_surface, text_rect)

def check_collision(rect1, rect2):
    """检查两个矩形是否碰撞"""
    return rect1.colliderect(rect2)

def clamp(value, min_value, max_value):
    """限制值在指定范围内"""
    return max(min_value, min(value, max_value))

def generate_enemy_wave(level, screen_width):
    """根据关卡生成敌人波次"""
    enemies = []
    rows = min(3 + level // 2, 6)  # 随关卡增加行数
    cols = min(8 + level, 12)      # 随关卡增加列数
    
    enemy_types = [1, 2, 3]
    for row in range(rows):
        for col in range(cols):
            x = 50 + col * 60
            y = 50 + row * 50
            # 不同行使用不同类型的敌人
            enemy_type = enemy_types[min(row, len(enemy_types) - 1)]
            enemies.append((x, y, enemy_type))
    
    return enemies

def get_high_score():
    """获取高分"""
    try:
        # Pygbag兼容：检查是否在Web环境中
        if platform.system() == 'Emscripten':
            # 在Web环境中，使用localStorage或默认值
            return 0
        else:
            with open('high_score.txt', 'r') as f:
                return int(f.read())
    except:
        return 0

def save_high_score(score):
    """保存高分"""
    try:
        # Pygbag兼容：检查是否在Web环境中
        if platform.system() != 'Emscripten':
            with open('high_score.txt', 'w') as f:
                f.write(str(score))
    except:
        pass