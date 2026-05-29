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
font = pygame.font.SysFont("Arial", 40)

# Bird settings
bird_x = 100
bird_y = HEIGHT // 2
bird_radius = 20

bird_velocity = 0
gravity = 0.5
jump_strength = -9

# Pipe settings
pipe_width = 80
pipe_gap = 180
pipe_speed = 4

pipes = []

# Score
score = 0


def create_pipe():
    height = random.randint(150, 450)

    top_pipe = pygame.Rect(WIDTH, 0, pipe_width, height)
    bottom_pipe = pygame.Rect(
        WIDTH,
        height + pipe_gap,
        pipe_width,
        HEIGHT - height - pipe_gap
    )

    return top_pipe, bottom_pipe


# Create first pipe
pipes.append(create_pipe())



def draw_bird():
    pygame.draw.circle(screen, YELLOW, (bird_x, int(bird_y)), bird_radius)



def draw_pipes():
    for top_pipe, bottom_pipe in pipes:
        pygame.draw.rect(screen, GREEN, top_pipe)
        pygame.draw.rect(screen, GREEN, bottom_pipe)



def move_pipes():
    global score

    for pipe_pair in pipes:
        pipe_pair[0].x -= pipe_speed
        pipe_pair[1].x -= pipe_speed

    # Remove old pipes
    if pipes and pipes[0][0].x < -pipe_width:
        pipes.pop(0)
        score += 1

    # Add new pipes
    if pipes and pipes[-1][0].x < WIDTH - 250:
        pipes.append(create_pipe())



def check_collision():
    bird_rect = pygame.Rect(
        bird_x - bird_radius,
        int(bird_y) - bird_radius,
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



def game_over():
    over_text = font.render("GAME OVER", True, BLACK)
    score_text = font.render(f"Final Score: {score}", True, BLACK)

    screen.blit(over_text, (WIDTH // 2 - 130, HEIGHT // 2 - 50))
    screen.blit(score_text, (WIDTH // 2 - 140, HEIGHT // 2 + 10))

    pygame.display.update()
    pygame.time.delay(3000)

    pygame.quit()
    sys.exit()


# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_velocity = jump_strength

    # Apply gravity
    bird_velocity += gravity
    bird_y += bird_velocity

    # Move pipes
    move_pipes()

    # Check collision
    if check_collision():
        game_over()

    # Draw everything
    screen.fill(SKY_BLUE)

    draw_bird()
    draw_pipes()
    show_score()

    pygame.display.update()
    clock.tick(FPS)
