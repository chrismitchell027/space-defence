import pygame
from math import sqrt

class Bullet:
    def __init__(self, x_start, y_start, direction_x, direction_y, radius, damage, penetration, scale, color=(255, 255, 255)):
        self.x = x_start
        self.y = y_start
        self.direction_x = direction_x
        self.direction_y = direction_y
        self.scale = scale
        self.speed = 3 * self.scale
        self.radius = radius * self.scale
        self.damage = damage
        self.penetration = penetration
        self.color = color
        self.enemies_hit = []
        
    def update(self):
        self.x += self.direction_x * self.speed
        self.y += self.direction_y * self.speed
        
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
        
    def delete(self, bullets):
        # Remove the bullet from the given list
        bullets.remove(self)
        
    def check_hit(self, enemies):
        distance = 255
        hit_info = {
            "Hit":False,
            "Target Died":False,
            "Died":False
        }
        for enemy in enemies:
            if enemy in self.enemies_hit:
                continue
            distance = sqrt((enemy.x - self.x) ** 2 + (enemy.y - self.y) ** 2)
            if distance <= enemy.radius + self.radius:
                hit_info["Target Died"] = enemy.take_damage(enemies, self.damage)
                hit_info["Hit"] = True
                self.penetration -= 1
                self.enemies_hit.append(enemy)
                if self.penetration <= 0:
                    hit_info["Died"] = True
                return hit_info
        return hit_info
        


    def check_off_screen(self, screen_width, screen_height, bullets):
        # Check if the bullet is off the screen
        if self.x < -self.radius or self.x > screen_width + self.radius or self.y < -self.radius or self.y > screen_height + self.radius:
            # If the bullet is off the screen, remove it from the given list
            self.delete(bullets)