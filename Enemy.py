import pygame, os
from math import sqrt
from random import randint

class Asteroid:
    def __init__(self, screen_width, screen_height, speed, health, damage, size_multiplier, sound_volume):
        # Load enemy image
        assets_dir = "assets"
        image_path = os.path.join(assets_dir, "asteroid.png")
        self.image = pygame.image.load(image_path)
        self.scale = screen_width / 800
        self.width, self.height = (self.image.get_width() * self.scale, self.image.get_height() * self.scale)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.radius = self.image.get_width() / 2
        self.speed = speed
        self.max_health = health
        self.health = self.max_health
        self.damage = damage
        self.sound_volume = sound_volume

        # Calculate the starting position
        if randint(0,1):
            self.x = randint(0 - self.radius, screen_width + self.radius)
            if randint(0, 1):
                self.y = screen_height + self.height
            else:
                self.y = -self.height
        else:
            self.y = randint(0 - self.height, screen_height + self.height)
            if randint(0, 1):
                self.x = screen_width + self.width
            else:
                self.x = -self.width

        # Calculate the direction from the enemy to the player
        self.direction_x = (screen_width // 2) - self.x
        self.direction_y = (screen_height // 2) - self.y
        
        # Normalize the direction vector
        direction_length = sqrt(self.direction_x ** 2 + self.direction_y ** 2)
        if direction_length != 0:
            self.direction_x /= direction_length
            self.direction_y /= direction_length

        

    def update(self):
        self.x += self.direction_x * self.speed
        self.y += self.direction_y * self.speed

    def check_reached_player(self, player_x, player_y, player_radius, asteroids):
        distance = sqrt((player_x - self.x) ** 2 + (player_y - self.y) ** 2)

        if distance <= player_radius + self.radius:
            self.delete(asteroids)
            return True

    def draw(self, surface):
        # Draw the image at its current position
        surface.blit(self.image, (self.x - self.radius, self.y - self.radius))

        # Draw health bar
        health_bar_width = 50 * self.scale
        health_bar_height = 5 * self.scale
        health_bar_rect = pygame.Rect(self.x - health_bar_width // 2, self.y + self.radius + 10, health_bar_width, health_bar_height)
        pygame.draw.rect(surface, (255, 0, 0), health_bar_rect)
        
        health_fill_width = health_bar_width * (self.health / self.max_health)
        health_fill_rect = pygame.Rect(self.x - health_bar_width // 2, self.y + self.radius + 10, health_fill_width, health_bar_height)
        pygame.draw.rect(surface, (0, 255, 0), health_fill_rect)

    def delete(self, asteroids):
        asteroids.remove(self)

    # Returns True if asteroid died
    def take_damage(self, asteroids, damage):
        sound = pygame.mixer.Sound("assets/destroy.wav")
        sound.set_volume(self.sound_volume)
        self.health = max(0, self.health - damage)
        died = False
        if self.health == 0:
            self.delete(asteroids)
            sound.play()
            died = True
            return died
        return died