import pygame
import random
import sys

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Screen
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Racing with Full Movement and Sound")

clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
RED = (200, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GOLD = (255, 215, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Font
font = pygame.font.SysFont(None, 36)

# Car and movement
car_width = 60
car_height = 100
player_speed = 5

# ✅ LOAD PLAYER CAR IMAGE (black car)
try:
    player_car = pygame.image.load("car.png").convert_alpha()
    player_car.set_colorkey((255, 255, 255))  # Remove white background
    player_car = pygame.transform.scale(player_car, (car_width, car_height))
except:
    print("car.jpg not found, using red rectangle")
    player_car = pygame.Surface((car_width, car_height))
    player_car.fill(RED)

# ✅ LOAD ENEMY CAR IMAGE (blue car)
try:
    enemy_car = pygame.image.load("enemy_car.png").convert_alpha()
    enemy_car.set_colorkey((255, 255, 255))  # Remove white background
    enemy_car = pygame.transform.scale(enemy_car, (car_width, car_height))
except:
    print("enemy_car.jpg not found, using blue rectangle")
    enemy_car = pygame.Surface((car_width, car_height))
    enemy_car.fill(BLUE)

# Player position
player_x = 170
player_y = HEIGHT - car_height - 10

# Enemy cars (multiple)
enemies = []
for i in range(3):
    enemies.append({
        'x': random.choice([60, 170, 280]),
        'y': -car_height * (i * 4 + 1)
    })

# Coins (multiple)
coins = []
for i in range(3):
    coins.append({
        'x': random.choice([60, 170, 280]) + car_width // 2,
        'y': -50 - i * 150
    })
coin_radius = 15

# Road line setup
road_line_y_positions = [i * 40 for i in range(15)]
road_line_speed = 9

# Score, level, game state
score = 0
high_score = 0
level = 1
base_enemy_speed = 6
base_coin_speed = 4
game_state = "PLAYING"

# Load background music
try:
    pygame.mixer.music.load("bg_music.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
except Exception as e:
    print("Background music error:", e)

# Load reverse sound
try:
    reverse_sound = pygame.mixer.Sound("reverse.wav")
    reverse_sound.set_volume(0.6)
except:
    reverse_sound = None
    print("reverse.wav not found")

# Dynamic background colors
background_colors = [(20, 20, 20), (40, 40, 80), (80, 80, 120), (120, 120, 160), (160, 160, 200)]
current_bg_color = background_colors[0]


def draw_text(text, size, color, x, y, center=True):
    font = pygame.font.SysFont(None, size)
    render = font.render(text, True, color)
    rect = render.get_rect(center=(x, y) if center else (x, y))
    screen.blit(render, rect)

def draw_button(rect, label):
    pygame.draw.rect(screen, WHITE, rect)
    draw_text(label, 24, BLACK, rect.centerx, rect.centery)

def reset_game():
    global player_x, player_y, score, level, enemies, coins, game_state, current_bg_color

    player_x = 170
    player_y = HEIGHT - car_height - 10
    score = 0
    level = 1
    game_state = "PLAYING"
    current_bg_color = background_colors[0]
    enemies = []
    for i in range(3):
        enemies.append({
            'x': random.choice([60, 170, 280]),
            'y': -car_height * (i * 4 + 1)
        })
    coins = []
    for i in range(3):
        coins.append({
            'x': random.choice([60, 170, 280]) + car_width // 2,
            'y': -50 - i * 150
        })
    pygame.mixer.music.play(-1)

# Game loop
running = True
while running:
    screen.fill(current_bg_color)

    # Scroll and draw road lines
    road_line_speed = 5 + (level - 1) * 0.3
    for i in range(len(road_line_y_positions)):
        road_line_y_positions[i] += road_line_speed
        if road_line_y_positions[i] > HEIGHT:
            road_line_y_positions[i] = -40
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 5, road_line_y_positions[i], 10, 20))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if game_state == "PLAYING":
                if event.key == pygame.K_ESCAPE:
                    game_state = "PAUSED"
                    pygame.mixer.music.pause()
            elif game_state == "PAUSED":
                if event.key == pygame.K_r:
                    game_state = "PLAYING"
                    pygame.mixer.music.unpause()
                elif event.key == pygame.K_RETURN:
                    reset_game()
            elif game_state == "GAME_OVER":
                if event.key == pygame.K_RETURN:
                    reset_game()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            # Placeholder for touch input (left/right/up/down buttons can be added here)

    keys = pygame.key.get_pressed()
    if game_state == "PLAYING":
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - car_width:
            player_x += player_speed
        if keys[pygame.K_UP] and player_y > 0:
            player_y -= player_speed
        if keys[pygame.K_DOWN] and player_y < HEIGHT - car_height:
            player_y += player_speed
            if reverse_sound:
                reverse_sound.play()

        # Move enemies
        for enemy in enemies:
            enemy['y'] += base_enemy_speed + (level - 1) * 0.5
            if enemy['y'] > HEIGHT:
                enemy['y'] = -car_height
                enemy['x'] = random.choice([60, 170, 280])
                score += 1

        # Move coins
        for coin in coins:
            coin['y'] += base_coin_speed + (level - 1) * 0.3
            if coin['y'] > HEIGHT:
                coin['y'] = -50
                coin['x'] = random.choice([60, 170, 280]) + car_width // 2

        # Level system
        level = score // 10 + 1

        # Collision detection
        player_rect = pygame.Rect(player_x, player_y, car_width, car_height)

        for enemy in enemies:
            enemy_rect = pygame.Rect(enemy['x'], enemy['y'], car_width, car_height)
            if player_rect.colliderect(enemy_rect):
                game_state = "GAME_OVER"
                pygame.mixer.music.stop()

        for coin in coins:
            coin_rect = pygame.Rect(coin['x'] - coin_radius, coin['y'] - coin_radius, coin_radius * 2, coin_radius * 2)
            if player_rect.colliderect(coin_rect):
                score += 5
                coin['y'] = -50
                coin['x'] = random.choice([60, 170, 280]) + car_width // 2

        if score > high_score:
            high_score = score

        # Draw objects
        screen.blit(player_car, (player_x, player_y))
        for enemy in enemies:
            screen.blit(enemy_car, (enemy['x'], enemy['y']))
        for coin in coins:
            pygame.draw.circle(screen, GOLD, (coin['x'], coin['y']), coin_radius)
        draw_text(f"Score: {score}", 30, WHITE, 10, 10, center=False)
        draw_text(f"High Score: {high_score}", 30, WHITE, 10, 40, center=False)
        draw_text(f"Level: {level}", 30, WHITE, 10, 70, center=False)

    elif game_state == "PAUSED":
        draw_text("PAUSED", 60, YELLOW, WIDTH // 2, HEIGHT // 2 - 50)
        draw_text("Press R to Resume", 30, WHITE, WIDTH // 2, HEIGHT // 2)
        draw_text("Press ENTER to Restart", 30, WHITE, WIDTH // 2, HEIGHT // 2 + 40)

    elif game_state == "GAME_OVER":
        draw_text("GAME OVER", 60, RED, WIDTH // 2, HEIGHT // 2 - 50)
        draw_text(f"Final Score: {score}", 30, WHITE, WIDTH // 2, HEIGHT // 2)
        draw_text(f"High Score: {high_score}", 30, WHITE, WIDTH // 2, HEIGHT // 2 + 30)
        draw_text("Press ENTER to Restart", 30, WHITE, WIDTH // 2, HEIGHT // 2 + 60)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
