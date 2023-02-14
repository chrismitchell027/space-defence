import pygame, os, math
from Bullet import Bullet
class Player:
    def __init__(self, screen_width, screen_height):
        # Load player image
        assets_dir = "assets"
        player_path = os.path.join(assets_dir, "player.png")
        self.image = pygame.image.load(player_path)
        
        # Set player position
        self.radius = 25
        self.x = screen_width // 2
        self.y = screen_height // 2
        
        # Set player health
        self.max_health = 100
        self.health = self.max_health
        
        # Set player shoot variables
        self.firerate = 5 # per second
        self.damage = 10 
        
    def draw(self, surface):
        # Draw player on surface
        rect = self.image.get_rect()
        rect.center = (self.x, self.y)
        surface.blit(self.image, rect)
        
        # Draw health bar
        health_bar_width = 50
        health_bar_height = 5
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
        bullet_radius = 4
        bullet_x = self.x + direction_x * (self.radius + bullet_radius)
        bullet_y = self.y + direction_y * (self.radius + bullet_radius)
        
        # Create the bullet
        bullet = Bullet(bullet_x, bullet_y, direction_x, direction_y, bullet_radius, self.damage)
        return bullet