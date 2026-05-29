import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen settings
WIDTH = 500
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Clock
clock = pygame.time.Clock()
FPS = 60

# Colors
SKY_BLUE = (135, 206, 235)
GREEN = (0, 200, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Font
font = pygame.font.SysFont("Arial", 35)

# Bird settings
bird_x = 100
bird_y = HEIGHT // 2
bird_radius = 20
bird_velocity = 0
gravity = 0.5
jump_power = -8

# Pipe settings
pipe_width = 80
pipe_gap = 180
pipe_speed = 4

pipes = []

# Score
score = 0

# Game state
game_over = False


def create_pipe():
    height = random.randint(100, 500)
    top_pipe = pygame.Rect(WIDTH, 0, pipe_width, height)
    bottom_pipe = pygame.Rect(
        WIDTH,
        height + pipe_gap,
        pipe_width,
        HEIGHT - height - pipe_gap
    )

    return top_pipe, bottom_pipe


# Add first pipe
pipes.append(create_pipe())


def draw_bird():
    pygame.draw.circle(screen, YELLOW, (bird_x, int(bird_y)), bird_radius)



def draw_pipes():
    for top_pipe, bottom_pipe in pipes:
        pygame.draw.rect(screen, GREEN, top_pipe)
        pygame.draw.rect(screen, GREEN, bottom_pipe)



def move_pipes():
    global score

    for pipe in pipes:
        pipe[0].x -= pipe_speed
        pipe[1].x -= pipe_speed

    # Remove off-screen pipes
    if pipes and pipes[0][0].x < -pipe_width:
        pipes.pop(0)
        score += 1

    # Add new pipes
    if pipes and pipes[-1][0].x < WIDTH - 250:
        pipes.append(create_pipe())



def check_collision():
    bird_rect = pygame.Rect(
        bird_x - bird_radius,
        bird_y - bird_radius,
        bird_radius * 2,
        bird_radius * 2
    )

    # Ground or ceiling collision
    if bird_y <= 0 or bird_y >= HEIGHT:
        return True

    # Pipe collision
    for top_pipe, bottom_pipe in pipes:
        if bird_rect.colliderect(top_pipe) or bird_rect.colliderect(bottom_pipe):
            return True

    return False



def show_score():
    text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(text, (20, 20))



def show_game_over():
    over_text = font.render("GAME OVER", True, BLACK)
    restart_text = font.render("Press SPACE to Restart", True, BLACK)

    screen.blit(over_text, (WIDTH // 2 - 120, HEIGHT // 2 - 40))
    screen.blit(restart_text, (WIDTH // 2 - 180, HEIGHT // 2 + 20))



def reset_game():
    global bird_y, bird_velocity, pipes, score, game_over

    bird_y = HEIGHT // 2
    bird_velocity = 0
    pipes = [create_pipe()]
    score = 0
    game_over = False


# Main game loop
while True:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_over:
                    reset_game()
                else:
                    bird_velocity = jump_power

    if not game_over:
        # Bird physics
        bird_velocity += gravity
        bird_y += bird_velocity

        # Move pipes
        move_pipes()

        # Collision check
        if check_collision():
            game_over =