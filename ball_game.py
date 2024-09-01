import pygame
import random
import time
import os

# Initialize Pygame
pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([1200, 1200])

# Initialize variables
ball_pos = [600, 600]
ball_speed = [0.75, 0.75]
ball_radius = 10
banana_pos = [random.randint(0, 1200), random.randint(0, 1200)]
butterfly_pos = None
butterfly_speed = 0.3
butterfly_active = False
bananas_eaten = 0
font = pygame.font.Font(None, 36)
highscore_file = "highscore.txt"

# Load high score from file
if os.path.exists(highscore_file):
    with open(highscore_file, "r") as file:
        highscore_data = file.read().split(',')
        highscore = int(highscore_data[0])
        highscore_name = highscore_data[1]
else:
    highscore = 0
    highscore_name = "Anonymous"

# Function to get player name
def get_player_name():
    player_name = ""
    input_active = True
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    player_name += event.unicode

        screen.fill((0, 0, 0))
        prompt_text = font.render("Enter your name: " + player_name, True, (255, 255, 255))
        screen.blit(prompt_text, (400, 600))
        pygame.display.flip()

    return player_name

# Run until the user asks to quit
running = True
game_start_time = time.time()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Setup keys for user input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        ball_pos[0] -= ball_speed[0]
    if keys[pygame.K_RIGHT]:
        ball_pos[0] += ball_speed[0]
    if keys[pygame.K_UP]:
        ball_pos[1] -= ball_speed[1]
    if keys[pygame.K_DOWN]:
        ball_pos[1] += ball_speed[1]

    ball_pos[0] = max(0, min(ball_pos[0], 1200))
    ball_pos[1] = max(0, min(ball_pos[1], 1200))

    ball_rect = pygame.Rect(ball_pos[0] - ball_radius, ball_pos[1] - ball_radius, ball_radius * 2, ball_radius * 2)
    banana_rect = pygame.Rect(banana_pos[0] - 25, banana_pos[1] - 25, 50, 50)
    if ball_rect.colliderect(banana_rect):
        banana_pos = [random.randint(0, 1200), random.randint(0, 1200)]
        bananas_eaten += 1
        ball_radius += 5

    if not butterfly_active and time.time() - game_start_time > 5:
        while True:
            butterfly_pos = [random.randint(0, 1200), random.randint(0, 1200)]
            butterfly_rect = pygame.Rect(butterfly_pos[0] - 25, butterfly_pos[1] - 25, 50, 50)
            if not butterfly_rect.colliderect(ball_rect):
                break
        butterfly_active = True

    if butterfly_active:
        butterfly_rect = pygame.Rect(butterfly_pos[0] - 25, butterfly_pos[1] - 25, 50, 50)
        new_x = butterfly_pos[0]
        new_y = butterfly_pos[1]
        if butterfly_pos[0] < ball_pos[0]:
            new_x += butterfly_speed
        if butterfly_pos[0] > ball_pos[0]:
            new_x -= butterfly_speed
        if butterfly_pos[1] < ball_pos[1]:
            new_y += butterfly_speed
        if butterfly_pos[1] > ball_pos[1]:
            new_y -= butterfly_speed
        butterfly_pos[0] = new_x
        butterfly_pos[1] = new_y
        if ball_rect.colliderect(butterfly_rect):
            running = False

    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, (0, 0, 255), ball_pos, ball_radius)
    pygame.draw.rect(screen, (255, 255, 0), banana_rect)
    if butterfly_active:
        pygame.draw.circle(screen, (255, 0, 255), butterfly_pos, 25)

    elapsed_game_time = int(time.time() - game_start_time)
    game_time_text = font.render(f'Game Time: {elapsed_game_time}s', True, (255, 255, 255))
    screen.blit(game_time_text, (10, 10))

    bananas_text = font.render(f'Bananas Eaten: {bananas_eaten}', True, (255, 255, 255))
    screen.blit(bananas_text, (10, 50))

    highscore_text = font.render(f'High Score: {highscore} by {highscore_name}', True, (255, 255, 255))
    screen.blit(highscore_text, (10, 90))

    pygame.display.flip()

if bananas_eaten > highscore:
    player_name = get_player_name()
    with open(highscore_file, "w") as file:
        file.write(f"{bananas_eaten},{player_name}")
    highscore = bananas_eaten
    highscore_name = player_name

score_screen_running = True
while score_screen_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            score_screen_running = False

    screen.fill((0, 0, 0))
    final_score_text = font.render(f'Final Score: {bananas_eaten}', True, (255, 255, 255))
    screen.blit(final_score_text, (500, 500))
    highscore_text = font.render(f'High Score: {highscore} by {highscore_name}', True, (255, 255, 255))
    screen.blit(highscore_text, (500, 550))
    pygame.display.flip()

pygame.quit()