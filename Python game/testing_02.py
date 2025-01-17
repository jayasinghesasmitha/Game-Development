import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PINK = (255, 105, 180)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Running Game")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Load assets
player_size = (50, 50)
player = pygame.Rect(100, SCREEN_HEIGHT - player_size[1] - 20, *player_size)

obstacle_size = (25, 25)
obstacles = []
obstacle_timer = 0

heart_size = (20, 20)
hearts = []
heart_timer = 0

# Game variables
GRAVITY = 1
jump_speed = -15
player_speed_y = 0
is_jumping = False
score = 0
hearts_collected = 0  # Variable to track collected hearts
font = pygame.font.Font(None, 36)

paused = False
game_over = False
game_won = False  # Variable to track if the player wins

# Function to draw the player as a stick figure
def draw_player(player_rect):
    pygame.draw.circle(screen, BLUE, (player_rect.centerx, player_rect.top + 15), 10)
    pygame.draw.line(screen, BLACK, (player_rect.centerx, player_rect.top + 25),
                     (player_rect.centerx, player_rect.top + 40), 3)
    pygame.draw.line(screen, BLACK, (player_rect.centerx, player_rect.top + 30),
                     (player_rect.centerx - 10, player_rect.top + 35), 2)
    pygame.draw.line(screen, BLACK, (player_rect.centerx, player_rect.top + 30),
                     (player_rect.centerx + 10, player_rect.top + 35), 2)
    pygame.draw.line(screen, BLACK, (player_rect.centerx, player_rect.top + 40),
                     (player_rect.centerx - 10, player_rect.bottom), 2)
    pygame.draw.line(screen, BLACK, (player_rect.centerx, player_rect.top + 40),
                     (player_rect.centerx + 10, player_rect.bottom), 2)

def draw_obstacles():
    for obstacle in obstacles:
        pygame.draw.rect(screen, RED, obstacle)

def draw_heart(x, y):
    pygame.draw.circle(screen, PINK, (x - 5, y), 10)
    pygame.draw.circle(screen, PINK, (x + 5, y), 10)
    pygame.draw.polygon(screen, PINK, [(x - 10, y + 5), (x + 10, y + 5), (x, y + 20)])

def draw_hearts():
    for heart in hearts:
        draw_heart(heart.x + heart.width // 2, heart.y + heart.height // 2)

def display_heart_bar(x, y, heart_count):
    for i in range(heart_count):
        draw_heart(x + i * 30, y)  # Draw hearts spaced 30 pixels apart

def move_objects():
    global score
    for obstacle in obstacles[:]:
        obstacle.x -= 5
        if obstacle.x < -obstacle.width:
            obstacles.remove(obstacle)
            score += 1

    for heart in hearts[:]:
        heart.x -= 5
        if heart.x < -heart.width:
            hearts.remove(heart)

def check_collision():
    for obstacle in obstacles:
        if player.colliderect(obstacle):
            return True
    return False

def check_heart_collection():
    global hearts_collected
    for heart in hearts[:]:
        if player.colliderect(heart):
            hearts.remove(heart)
            hearts_collected += 1  # Increment heart count

# Main game loop
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_jumping and not paused and not game_over and not game_won:
                is_jumping = True
                player_speed_y = jump_speed
            if event.key == pygame.K_p and not game_over and not game_won:
                paused = not paused
            if event.key == pygame.K_r and (game_over or game_won):
                # Reset game variables for restart
                game_over = False
                game_won = False
                paused = False
                obstacles.clear()
                hearts.clear()
                score = 0
                hearts_collected = 0
                player.y = SCREEN_HEIGHT - player_size[1] - 20

    if not paused and not game_over and not game_won:
        # Player movement
        if is_jumping:
            player_speed_y += GRAVITY
            player.y += player_speed_y
            if player.y >= SCREEN_HEIGHT - player.height - 20:
                player.y = SCREEN_HEIGHT - player.height - 20
                is_jumping = False

        # Obstacle generation
        obstacle_timer += 1
        if obstacle_timer > 50:
            obstacle_timer = 0
            obstacle_x = SCREEN_WIDTH
            obstacle_y = SCREEN_HEIGHT - obstacle_size[1] - 20
            obstacles.append(pygame.Rect(obstacle_x, obstacle_y, *obstacle_size))

        # Heart generation
        heart_timer += 1
        if heart_timer > 150:
            heart_timer = 0
            heart_x = random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 200)
            heart_y = random.randint(100, SCREEN_HEIGHT - 50)
            hearts.append(pygame.Rect(heart_x, heart_y, *heart_size))

        # Move and draw objects
        move_objects()
        draw_obstacles()
        draw_hearts()

        # Draw player
        draw_player(player)

        # Check for collisions and collections
        if check_collision():
            game_over = True
        check_heart_collection()

        # Check win condition
        if hearts_collected >= 1:
            game_won = True

        # Display score
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # Display heart bar
        display_heart_bar(10, 50, hearts_collected)

    elif paused:
        pause_text = font.render("Game Paused. Press P to Resume", True, RED)
        screen.blit(pause_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))

    elif game_over:
        game_over_text = font.render("Game Over! Press R to Restart", True, RED)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
        score_text = font.render(f"Final Score: {score}", True, BLACK)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50))
        heart_text = font.render(f"Hearts Collected: {hearts_collected}", True, PINK)
        screen.blit(heart_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 90))

    elif game_won:
        win_text = font.render("I Love You! Press R to Restart", True, GREEN)
        screen.blit(win_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)

pygame.quit()
