import pygame
import os
from Player import Player
from Enemy import *

# Set up the display
pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Set up the font
font = pygame.font.SysFont("Arial", 50)

# Load the background image
assets_dir = "assets"
background_path = os.path.join(assets_dir, "background.png")
background = pygame.image.load(background_path)

# Load the clock
clock = pygame.time.Clock()

# Load the sounds
sound_volume = 0.25
sounds = {"shoot": pygame.mixer.Sound("assets/shoot.wav"),
    "select": pygame.mixer.Sound("assets/select.wav"),
    "hit": pygame.mixer.Sound("assets/hit.wav"),
    "hurt": pygame.mixer.Sound("assets/hurt.wav")
}
for sound in sounds:
    sounds[sound].set_volume(sound_volume)

def menu():
    
    # Create the Play Button surface
    button_width = 200
    button_height = 100
    button_surface = pygame.Surface((button_width, button_height))
    button_surface.fill((0, 0, 0)) # Black background
    button_rect = button_surface.get_rect(center=(screen_width//2,screen_height//2))

    # Draw the text on the button
    text = font.render("PLAY", True, (255, 255, 255)) # White text
    text_rect = text.get_rect(center=(button_width // 2, button_height // 2))
    button_surface.blit(text, text_rect)

    running = True
    while running:
        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_rect.collidepoint(event.pos):
                    sounds["select"].play()
                    play()

        # Set the background image as the background of the screen
        screen.blit(background, (0, 0))
        screen.blit(button_surface, button_rect)

        pygame.display.flip()
    


def play():
    # Initialize the player and bullets
    player = Player(screen_width, screen_height)
    bullets = []
    can_shoot = False
    delay = 1000 / player.firerate # converts firerate to milliseconds
    delay_timer = pygame.time.get_ticks()

    # Initialize the enemies
    asteroids = []

    # Game loop
    running = True
    while running:
        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    asteroids.append(Asteroid(screen_width, screen_height))

        # Check if the left mouse button is held down to shoot
        if pygame.mouse.get_pressed()[0] and can_shoot: # 0 = left button
            mouse_x, mouse_y = pygame.mouse.get_pos()
            bullets.append(player.shoot(mouse_x, mouse_y))
            can_shoot = False
            delay_timer = pygame.time.get_ticks()
            sounds["shoot"].play()

        if not can_shoot:
            elapsed_time = pygame.time.get_ticks() - delay_timer
            if elapsed_time >= delay:
                can_shoot = True

        # Update the screen
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        player.draw(screen)
        for bullet in bullets:
            bullet.update()
            if bullet.check_hit(asteroids):
                bullet.delete(bullets)
                sounds["hit"].play()
            bullet.check_off_screen(screen_width, screen_height, bullets)
            bullet.draw(screen)

        for asteroid in asteroids:
            asteroid.update()
            if asteroid.check_reached_player(screen_width // 2, screen_height // 2, player.radius, asteroids):
                player.take_damage(asteroid.damage)
                sounds["hurt"].play()
            asteroid.draw(screen)

        pygame.display.flip()

        clock.tick(60) # Set game to 60FPS

# Start the game
menu()

# Quit the game
pygame.quit()
