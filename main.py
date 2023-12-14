import pygame
import os
import math
import random
from Player import Player
from Enemy import Asteroid
from Button import Button
from Label import Label

# Set up the display
pygame.init()
screen_width, screen_height = 1600, 1200
scale = screen_width / 800
screen = pygame.display.set_mode((screen_width, screen_height))

# Set up the font
font_size = int(50 * scale)
font = pygame.font.SysFont("Arial", font_size)

# Load the background image
assets_dir = "assets"
background_path = os.path.join(assets_dir, "background.png")
background = pygame.image.load(background_path)
background = pygame.transform.scale(background, (screen_width, screen_height))

# Load the clock
clock = pygame.time.Clock()

# Load the sounds
sound_volume = 0.15
sounds = {"shoot": pygame.mixer.Sound("assets/shoot.wav"),
    "select": pygame.mixer.Sound("assets/select.wav"),
    "hit": pygame.mixer.Sound("assets/hit.wav"),
    "hurt": pygame.mixer.Sound("assets/hurt.wav"),
    "powerup": pygame.mixer.Sound("assets/powerup.wav")
}
for sound in sounds:
    sounds[sound].set_volume(sound_volume)

# variables for enemy spawning
initial_spawn_interval_ms = 2000
minimum_spawn_interval_ms = 100



def calculate_difficulty(current_time):
    # Constants for the difficulty function
    a = 1
    b = 0.125
    time_in_minutes = current_time / 60000 # milliseoncds -> minutes
    difficulty = a * math.exp(b * time_in_minutes)
    return difficulty

def spawn_asteroid(asteroids, difficulty):
    multipliers = [0.5, 1, 2]
    type = random.choice(multipliers)
    speed = 1 * round(difficulty,1) * (1 / type)
    health = 20 * round(difficulty,1) * type
    damage = 5 * round(difficulty,1) * type
    size_multiplier = round(1 / difficulty, 1) * type
    asteroids.append(Asteroid(screen_width, screen_height, speed, health, damage, size_multiplier, sound_volume))

def get_spawn_interval(difficulty):
    new_spawn_interval = max(initial_spawn_interval_ms / difficulty, minimum_spawn_interval_ms)
    return new_spawn_interval

def upgrade_menu(screen, player):
    running = True
    # define button variables
    text_color = (0, 0, 0) # black
    button_color = (255, 255, 255) # white
    button_size = (300 * scale, 75 * scale)
    # define all upgrades
    upgrades = [
        {"name": "Damage", "function": player.upgrade_damage},
        {"name": "Fire Rate", "function": player.upgrade_firerate},
        {"name": "Max Health", "function": player.upgrade_max_health},
        {"name": "Health Pack", "function": player.upgrade_health_pack},
        {"name": "Bullet Size", "function": player.upgrade_bullet_radius},
        {"name": "Bullet Penetration", "function": player.upgrade_penetration}
    ]

    selected_upgrades = random.sample(upgrades, 3)

    buttons = [
        Button(f"{upgrade['name']} [{player.upgrades[upgrade['name']]}]", font, text_color, upgrade["function"], top_left=((screen_width // 2) - (150 * scale), (screen_height // 2) + ((i * 100) - 150) * scale), bg_color=button_color,size=button_size)
        for i, upgrade in enumerate(selected_upgrades)
    ]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            for button in buttons:
                if button.check_hit(event):
                    button.function()
                    return

        #screen.fill((0, 0, 0))  # Clear the screen

        # Draw buttons
        for button in buttons:
            button.draw(screen)

        pygame.display.flip()
        clock.tick(60)


def menu():
    button_width = 200 * scale
    button_height = 100 * scale
    play_button = Button("PLAY", font, (255, 255, 255), play, center=(screen_width//2, screen_height//2), bg_color=(0, 0, 0), size=(button_width, button_height), anti_aliasing=True)
    running = True
    while running:
        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if play_button.check_hit(event):
                play_button.function()

        # Set the background image as the background of the screen
        screen.blit(background, (0, 0))
        play_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)
    


def play():
    # Initialize the player and bullets
    player = Player(screen_width, screen_height)
    bullets = []
    can_shoot = False
    delay = 1000 / player.firerate # converts firerate to milliseconds
    delay_timer = pygame.time.get_ticks()

    # Initialize the enemies
    asteroids = []

    # Variables for enemy spawning
    spawn_time = 0

    # xp bar variables and objects
    xp_bar_width = 200 * scale
    xp_bar_height = 20 * scale
    xp_bar_x = (screen_width - xp_bar_width) // 2
    xp_bar_y = 10 * scale
    xp_background_rect = pygame.Rect(xp_bar_x, xp_bar_y, xp_bar_width, xp_bar_height)

    # level label variables
    level_label_x = xp_background_rect.topright[0] + 10 * scale
    level_label_y = xp_background_rect.topright[1]

    level_label_font_size = int(18 * scale)
    level_label_font = pygame.font.SysFont("Arial", level_label_font_size)
    # Game loop
    running = True
    while running:
        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

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

        # Spawn enemies
        current_time = pygame.time.get_ticks()
        difficulty = calculate_difficulty(current_time)
        spawn_interval = get_spawn_interval(difficulty)
        if current_time - spawn_time > spawn_interval:
            spawn_asteroid(asteroids, difficulty)
            spawn_time = current_time

        # Check if the player should level up
        if player.check_for_level_up():
            upgrade_menu(screen, player)
            delay = 1000 / player.firerate # update firerate in case of firerate upgrade

        # Update the screen
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        player.draw(screen)


        # Update the asteroids
        for asteroid in asteroids:
            asteroid.update()
            if asteroid.check_reached_player(screen_width // 2, screen_height // 2, player.radius, asteroids):
                player.take_damage(asteroid.damage)
                sounds["hurt"].play()
            asteroid.draw(screen)

        # Update the bullets
        for bullet in bullets:
            bullet.update()
            hit_info = bullet.check_hit(asteroids)
            if hit_info["Hit"]:
                sounds["hit"].play()
            # if the enemy died give the player some xp
            if hit_info["Target Died"]:
                difficulty = calculate_difficulty(current_time)
                player.xp += round(difficulty ** 2)
            if hit_info["Died"]:
                bullet.delete(bullets)
            bullet.check_off_screen(screen_width, screen_height, bullets)
            bullet.draw(screen)

        # Draw the XP bar
        pygame.draw.rect(screen, (0, 0, 0), xp_background_rect)
        xp_progress = player.xp / player.xp_needed_to_level_up
        xp_foreground_width = xp_progress * xp_bar_width
        xp_foreground_width = min(xp_foreground_width, xp_bar_width)
        xp_foreground_rect = pygame.Rect(xp_bar_x, xp_bar_y, xp_foreground_width, xp_bar_height)
        pygame.draw.rect(screen, (0, 255, 0), xp_foreground_rect)

        level_label = Label(f"Level: {player.level}", level_label_font, (255, 255, 255), top_left=(level_label_x, level_label_y))
        level_label.draw(screen)

        pygame.display.flip()

        clock.tick(60) # Set game to 60FPS

# Start the game
menu()

# Quit the game
pygame.quit()
