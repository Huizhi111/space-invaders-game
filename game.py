import pygame
import random
from entities import Player, Enemy, Bullet, Explosion, PowerUp
from utils import draw_text, generate_enemy_wave, get_high_score, save_high_score

class Game:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.reset()
    
    def reset(self):
        """重置游戏状态"""
        self.player = Player(self.screen_width // 2 - 25, self.screen_height - 70)
        self.enemies = []
        self.player_bullets = []
        self.enemy_bullets = []
        self.explosions = []
        self.power_ups = []
        self.level = 1
        self.game_state = "menu"  # menu, playing, game_over, level_complete
        self.last_enemy_spawn = pygame.time.get_ticks()
        self.enemy_spawn_delay = 1000
        self.spawn_wave()
        self.high_score = get_high_score()
        self.font = pygame.font.Font(None, 36)
        self.large_font = pygame.font.Font(None, 72)
    
    def spawn_wave(self):
        """生成敌人波次"""
        wave_data = generate_enemy_wave(self.level, self.screen_width)
        for x, y, enemy_type in wave_data:
            self.enemies.append(Enemy(x, y, enemy_type))
    
    def handle_events(self, events):
        """处理游戏事件"""
        for event in events:
            if event.type == pygame.QUIT:
                return False
            
            if self.game_state == "menu":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.game_state = "playing"
            
            elif self.game_state == "playing":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bullet = self.player.shoot()
                        if bullet:
                            self.player_bullets.append(bullet)
            
            elif self.game_state == "game_over":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.reset()
                        self.game_state = "playing"
            
            elif self.game_state == "level_complete":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.level += 1
                        self.enemies = []
                        self.player_bullets = []
                        self.enemy_bullets = []
                        self.spawn_wave()
                        self.game_state = "playing"
        
        return True
    
    def update(self):
        """更新游戏状态"""
        if self.game_state != "playing":
            return
        
        # 更新玩家
        keys = pygame.key.get_pressed()
        self.player.update(keys, self.screen_width)
        
        # 更新敌人
        if self.enemies:
            # 检查敌人是否需要改变方向
            change_direction = False
            for enemy in self.enemies:
                enemy.update()
                # 敌人射击
                if random.random() < 0.01:  # 1% 的概率射击
                    bullet = enemy.shoot()
                    if bullet:
                        self.enemy_bullets.append(bullet)
                # 检查是否到达屏幕边缘
                if enemy.x <= 0 or enemy.x >= self.screen_width - enemy.width:
                    change_direction = True
            
            if change_direction:
                for enemy in self.enemies:
                    enemy.change_direction()
        
        # 更新子弹
        for bullet in self.player_bullets[:]:
            bullet.update()
            if bullet.y < 0:
                self.player_bullets.remove(bullet)
        
        for bullet in self.enemy_bullets[:]:
            bullet.update()
            if bullet.y > self.screen_height:
                self.enemy_bullets.remove(bullet)
        
        # 更新爆炸效果
        for explosion in self.explosions[:]:
            explosion.update()
            if not explosion.active:
                self.explosions.remove(explosion)
        
        # 更新电源
        for power_up in self.power_ups[:]:
            power_up.update()
            if power_up.y > self.screen_height:
                self.power_ups.remove(power_up)
        
        # 碰撞检测
        self.check_collisions()
        
        # 检查游戏状态
        if not self.enemies:
            self.game_state = "level_complete"
        
        if self.player.lives <= 0:
            if self.player.score > self.high_score:
                save_high_score(self.player.score)
                self.high_score = self.player.score
            self.game_state = "game_over"
    
    def check_collisions(self):
        """检查碰撞"""
        # 玩家子弹与敌人碰撞
        for bullet in self.player_bullets[:]:
            for enemy in self.enemies[:]:
                if bullet.rect.colliderect(enemy.rect):
                    self.player_bullets.remove(bullet)
                    self.enemies.remove(enemy)
                    self.explosions.append(Explosion(enemy.x + enemy.width // 2, enemy.y + enemy.height // 2))
                    self.player.score += enemy.points
                    # 随机掉落电源
                    if random.random() < 0.1:  # 10% 的概率掉落
                        power_type = random.randint(0, 2)
                        self.power_ups.append(PowerUp(enemy.x + enemy.width // 2 - 15, enemy.y + enemy.height, power_type))
                    break
        
        # 敌人子弹与玩家碰撞
        for bullet in self.enemy_bullets[:]:
            if bullet.rect.colliderect(self.player.rect):
                self.enemy_bullets.remove(bullet)
                self.player.lives -= 1
                self.explosions.append(Explosion(self.player.x + self.player.width // 2, self.player.y + self.player.height // 2))
        
        # 敌人与玩家碰撞
        for enemy in self.enemies[:]:
            if enemy.rect.colliderect(self.player.rect):
                self.enemies.remove(enemy)
                self.player.lives -= 1
                self.explosions.append(Explosion(enemy.x + enemy.width // 2, enemy.y + enemy.height // 2))
        
        # 玩家与电源碰撞
        for power_up in self.power_ups[:]:
            if power_up.rect.colliderect(self.player.rect):
                self.power_ups.remove(power_up)
                if power_up.power_type == 0:  # 速度提升
                    self.player.velocity += 1
                elif power_up.power_type == 1:  # 生命恢复
                    if self.player.lives < 3:
                        self.player.lives += 1
                elif power_up.power_type == 2:  # 火力增强
                    self.player.shoot_delay = max(100, self.player.shoot_delay - 50)
    
    def draw(self, screen):
        """绘制游戏"""
        screen.fill((0, 0, 0))
        
        if self.game_state == "menu":
            draw_text(screen, "太空侵略者", self.large_font, (255, 255, 255), self.screen_width // 2, self.screen_height // 2 - 50)
            draw_text(screen, "按空格键开始游戏", self.font, (255, 255, 255), self.screen_width // 2, self.screen_height // 2 + 50)
            draw_text(screen, f"最高分: {self.high_score}", self.font, (255, 255, 255), self.screen_width // 2, self.screen_height // 2 + 100)
        
        elif self.game_state == "playing":
            # 绘制玩家
            self.player.draw(screen)
            
            # 绘制敌人
            for enemy in self.enemies:
                enemy.draw(screen)
            
            # 绘制子弹
            for bullet in self.player_bullets:
                bullet.draw(screen)
            
            for bullet in self.enemy_bullets:
                bullet.draw(screen)
            
            # 绘制爆炸效果
            for explosion in self.explosions:
                explosion.draw(screen)
            
            # 绘制电源
            for power_up in self.power_ups:
                power_up.draw(screen)
            
            # 绘制游戏信息
            draw_text(screen, f"分数: {self.player.score}", self.font, (255, 255, 255), 100, 30)
            draw_text(screen, f"生命: {self.player.lives}", self.font, (255, 255, 255), self.screen_width - 100, 30)
            draw_text(screen, f"关卡: {self.level}", self.font, (255, 255, 255), self.screen_width // 2, 30)
        
        elif self.game_state == "game_over":
            draw_text(screen, "游戏结束", self.large_font, (255, 0, 0), self.screen_width // 2, self.screen_height // 2 - 50)
            draw_text(screen, f"最终分数: {self.player.score}", self.font, (255, 255, 255), self.screen_width // 2, self.screen_height // 2)
            draw_text(screen, f"最高分: {self.high_score}", self.font, (255, 255, 255), self.screen_width // 2, self.screen_height // 2 + 50)
            draw_text(screen, "按空格键重新开始", self.font, (255, 255, 255), self.screen_width // 2, self.screen_height // 2 + 100)
        
        elif self.game_state == "level_complete":
            draw_text(screen, "关卡完成!", self.large_font, (0, 255, 0), self.screen_width // 2, self.screen_height // 2 - 50)
            draw_text(screen, f"分数: {self.player.score}", self.font, (255, 255, 255), self.screen_width // 2, self.screen_height // 2)
            draw_text(screen, f"下一关: {self.level + 1}", self.font, (255, 255, 255), self.screen_width // 2, self.screen_height // 2 + 50)
            draw_text(screen, "按空格键进入下一关", self.font, (255, 255, 255), self.screen_width // 2, self.screen_height // 2 + 100)
        
        pygame.display.flip()