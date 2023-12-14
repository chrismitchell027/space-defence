import pygame, os, math
from Bullet import Bullet
class Player:
    def __init__(self, screen_width, screen_height):
        # Load player image
        assets_dir = "assets"
        player_path = os.path.join(assets_dir, "player.png")
        self.scale = screen_width / 800
        self.image = pygame.image.load(player_path)
        self.width, self.height = (self.image.get_width() * self.scale, self.image.get_height() * self.scale)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        # Set player position
        self.radius = 25 * self.scale
        self.x = screen_width // 2
        self.y = screen_height // 2
        
        # Set Initial Player Stats
        self.initial_max_health = 100
        self.initial_firerate = 1.8 # per second
        self.initial_damage = 10
        self.initial_bullet_size = 4
        self.initial_level = 1
        self.initial_bullet_penetration = 1
        self.upgrades = {
            "Damage":0,
            "Fire Rate":0,
            "Max Health":0,
            "Health Pack":0,
            "Bullet Size":0,
            "Bullet Penetration":0
        }
        # Set player health
        self.max_health = self.initial_max_health
        self.health = self.max_health
        
        # Set player shoot variables
        self.firerate = self.initial_firerate
        self.damage = self.initial_damage
        self.bullet_radius = self.initial_bullet_size
        self.bullet_penetration = self.initial_bullet_penetration

        # Set player experience variables
        self.level = self.initial_level
        self.xp = 0.0
        self.xp_needed_to_level_up = self.calculate_xp_needed_to_level_up()

    def draw(self, surface):
        # Draw player on surface
        rect = self.image.get_rect()
        rect.center = (self.x, self.y)
        surface.blit(self.image, rect)
        
        # Draw health bar
        health_bar_width = 50 * self.scale
        health_bar_height = 5 * self.scale
        health_bar_rect = pygame.Rect(self.x - health_bar_width // 2, self.y + self.radius + 10, health_bar_width, health_bar_height)
        pygame.draw.rect(surface, (255, 0, 0), health_bar_rect)
        
        health_fill_width = health_bar_width * (self.health / self.max_health)
        health_fill_rect = pygame.Rect(self.x - health_bar_width // 2, self.y + self.radius + 10, health_fill_width, health_bar_height)
        pygame.draw.rect(surface, (0, 255, 0), health_fill_rect)
        
    def take_damage(self, damage):
        # Reduce player health by damage amount
        self.health = max(0, self.health - damage)
        
    def shoot(self, mouse_x, mouse_y):
        # Calculate the direction from the player to the mouse
        direction_x = mouse_x - self.x
        direction_y = mouse_y - self.y
        
        # Normalize the direction vector
        direction_length = math.sqrt(direction_x ** 2 + direction_y ** 2)
        if direction_length != 0:
            direction_x /= direction_length
            direction_y /= direction_length
        
        # Calculate the position of the bullet
        bullet_radius = self.bullet_radius
        bullet_x = self.x + direction_x * (self.radius + bullet_radius)
        bullet_y = self.y + direction_y * (self.radius + bullet_radius)
        
        # Create the bullet
        bullet = Bullet(bullet_x, bullet_y, direction_x, direction_y, bullet_radius, self.damage, self.bullet_penetration, self.scale)
        return bullet

    def calculate_xp_needed_to_level_up(self):
        # constants for xp function
        a = 5
        b = 0.125
        xp_needed = a * math.exp(b * self.level)
        return xp_needed

    def upgrade_health_pack(self):
        # restores 50 health
        self.health = min(self.health + 50, self.max_health)
        self.upgrades["Health Pack"] += 1
        
    def upgrade_max_health(self):
        # 20 point increase per level
        self.max_health += 10
        self.health += 10
        self.upgrades["Max Health"] += 1
    
    def upgrade_firerate(self):
        # 20% increase per level
        self.firerate *= 1.2
        self.upgrades["Fire Rate"] += 1
    
    def upgrade_damage(self):
        # 20% increase per level
        self.damage *= 1.2
        self.upgrades["Damage"] += 1

    def upgrade_bullet_radius(self):
        # +1 radius per level
        self.bullet_radius += self.scale
        self.upgrades["Bullet Size"] += 1

    def upgrade_penetration(self):
        # +1 penetration per level
        self.bullet_penetration += 1
        self.upgrades["Bullet Penetration"] += 1

    def check_for_level_up(self):
        if self.xp >= self.xp_needed_to_level_up:
            self.level += 1
            self.xp -= self.xp_needed_to_level_up
            self.xp_needed_to_level_up = self.calculate_xp_needed_to_level_up()
            return True
        return False