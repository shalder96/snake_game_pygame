import pygame
import sys
import random
import pygame.mixer

# ---------- CONFIG ----------
CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
WIDTH = CELL_SIZE * GRID_WIDTH
HEIGHT = CELL_SIZE * GRID_HEIGHT

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 120, 0)
RED = (200, 0, 0)
GRAY = (40, 40, 40)

# ---------- HELPER FUNCTIONS ----------
def spawn_food(snake):
    """Return random position not on snake."""
    while True:
        x = random.randrange(0, GRID_WIDTH) * CELL_SIZE
        y = random.randrange(0, GRID_HEIGHT) * CELL_SIZE
        if (x, y) not in snake:
            return (x, y)

def draw_rect_border(surface, rect, color_border=(0,0,0), border=1):
    pygame.draw.rect(surface, color_border, rect, border)

# ---------- MAIN FUNCTION ----------
def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("🐍 Snake Game — Wrap Around Mode")
    clock = pygame.time.Clock()
    eat_sound = pygame.mixer.Sound("assets/eat.mp3")
    game_over_sound = pygame.mixer.Sound("assets/game_over.mp3")

    font = pygame.font.SysFont(None, 28)
    big_font = pygame.font.SysFont(None, 40)

    def new_game():
        start_x = (GRID_WIDTH // 2) * CELL_SIZE
        start_y = (GRID_HEIGHT // 2) * CELL_SIZE
        snake = [
            (start_x, start_y),
            (start_x - CELL_SIZE, start_y),
            (start_x - 2 * CELL_SIZE, start_y)
        ]
        direction = (1, 0)
        food = spawn_food(snake)
        score = 0
        base_speed = 2  # Start speed (FPS)
        return snake, direction, food, score, base_speed

    snake, direction, food, score, speed = new_game()
    game_over = False

    while True:
        # ----- EVENTS -----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # Movement
                if event.key in (pygame.K_UP, pygame.K_w) and direction != (0, 1):
                    direction = (0, -1)
                elif event.key in (pygame.K_DOWN, pygame.K_s) and direction != (0, -1):
                    direction = (0, 1)
                elif event.key in (pygame.K_LEFT, pygame.K_a) and direction != (1, 0):
                    direction = (-1, 0)
                elif event.key in (pygame.K_RIGHT, pygame.K_d) and direction != (-1, 0):
                    direction = (1, 0)

                elif event.key == pygame.K_r and game_over:
                    snake, direction, food, score, speed = new_game()
                    game_over = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        if not game_over:
            # ----- UPDATE -----
            head_x, head_y = snake[0]
            dx, dy = direction

            # Move + wrap around
            new_x = (head_x + dx * CELL_SIZE) % WIDTH
            new_y = (head_y + dy * CELL_SIZE) % HEIGHT
            new_head = (new_x, new_y)

            # Check self collision
            if new_head in snake:
                game_over = True
                game_over_sound.play()

            else:
                snake.insert(0, new_head)

                # Eat food
                if new_head == food:
                    score += 1
                    food = spawn_food(snake)
                    eat_sound.play()
                    # Speed increases slightly with each food eaten (max 20)
                    speed = min(2 + score * 0.1, 20)
                else:
                    snake.pop()

        # ----- DRAW -----
        screen.fill(BLACK)

        # Grid
        for x in range(0, WIDTH, CELL_SIZE):
            pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, CELL_SIZE):
            pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

        # Snake
        for i, (x, y) in enumerate(snake):
            color = DARK_GREEN if i == 0 else GREEN
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, color, rect)
            draw_rect_border(screen, rect, (0, 0, 0), 1)

        # Food
        food_rect = pygame.Rect(food[0], food[1], CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, RED, food_rect)
        draw_rect_border(screen, food_rect, (0, 0, 0), 1)

        # Score
        score_text = font.render(f"Score: {score}", True, WHITE)
        speed_text = font.render(f"Speed: {round(speed,1)}", True, WHITE)
        screen.blit(score_text, (8, 8))
        screen.blit(speed_text, (WIDTH - 120, 8))

        # Game over
        if game_over:
            over_surf = big_font.render("GAME OVER", True, WHITE)
            info_surf = font.render("Press R to Restart or Q to Quit", True, WHITE)
            rect_over = over_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
            rect_info = info_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
            screen.blit(over_surf, rect_over)
            screen.blit(info_surf, rect_info)

        pygame.display.flip()
        clock.tick(max(1, int(speed)))

if __name__ == "__main__":
    main()
