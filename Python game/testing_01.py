import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Game")

# Clock and font
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Player setup
player_size = 50
player_x = WIDTH // 2
player_y = HEIGHT - player_size - 10
player_speed = 5

# Falling objects setup
falling_objects = []
object_size = 30

# Score and misses
score = 0
misses = 0
max_misses = 10

# Game state variables
running = True
game_over = False
paused = False
difficulty_selected = False
difficulty = None

# Difficulty settings
difficulty_settings = {
    "Easy": {"fall_speed": 3, "spawn_rate": 30},
    "Medium": {"fall_speed": 5, "spawn_rate": 20},
    "Hard": {"fall_speed": 7, "spawn_rate": 10},
}

while running:
    screen.fill(WHITE)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Difficulty selection screen
    if not difficulty_selected:
        title_text = font.render("Select Difficulty: 1. Easy  2. Medium  3. Hard", True, BLUE)
        screen.blit(title_text, (WIDTH // 2 - 250, HEIGHT // 2 - 20))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            difficulty = "Easy"
            difficulty_selected = True
        elif keys[pygame.K_2]:
            difficulty = "Medium"
            difficulty_selected = True
        elif keys[pygame.K_3]:
            difficulty = "Hard"
            difficulty_selected = True

    elif not paused and not game_over:
        # Get difficulty settings
        fall_speed = difficulty_settings[difficulty]["fall_speed"]
        spawn_rate = difficulty_settings[difficulty]["spawn_rate"]

        # Get pressed keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
            player_x += player_speed
        if keys[pygame.K_p]:
            paused = not paused  

        # Spawn falling objects
        if random.randint(1, spawn_rate) == 1:
            falling_objects.append([random.randint(0, WIDTH - object_size), 0])

        # Move and draw falling objects
        for obj in falling_objects[:]:
            obj[1] += fall_speed
            if obj[1] > HEIGHT:
                falling_objects.remove(obj)
                misses += 1
                if misses >= max_misses:
                    game_over = True
            elif (
                obj[0] < player_x < obj[0] + object_size
                or obj[0] < player_x + player_size < obj[0] + object_size
            ):
                if player_y < obj[1] + object_size < player_y + player_size:
                    falling_objects.remove(obj)
                    score += 1
            pygame.draw.rect(screen, RED, (*obj, object_size, object_size))

        # Draw player
        pygame.draw.rect(screen, BLUE, (player_x, player_y, player_size, player_size))

        # Display score
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # Display misses bar
        pygame.draw.rect(screen, BLACK, (10, 50, 200, 20))  
        pygame.draw.rect(screen, GREEN, (10, 50, 20 * (max_misses - misses), 20))  
        misses_text = font.render(f"Misses: {misses}/{max_misses}", True, BLACK)
        screen.blit(misses_text, (220, 45))

        pause_text = font.render(f"To pause the game press P", True, BLUE)
        screen.blit(pause_text, (450, 10))

    elif paused:
        # Display pause message in the current window
        pause_text = font.render("Game Paused. Press P to Resume", True, RED)
        screen.blit(pause_text, (WIDTH // 2 - 200, HEIGHT // 2 - 20))

    elif game_over:
        # Game Over screen
        game_over_text = font.render("Game Over! Press R to Restart", True, RED)
        screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2))
        restart_text = font.render(f"Final Score: {score}", True, BLACK)
        screen.blit(restart_text, (WIDTH // 2 - 100, HEIGHT // 2 + 50))

        # Restart game
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            game_over = False
            paused = False
            falling_objects.clear()
            score = 0
            misses = 0
            player_x = WIDTH // 2
            difficulty_selected = False

    # Update display
    pygame.display.flip()
    clock.tick(30)

# Quit Pygame
pygame.quit()
