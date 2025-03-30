import pygame
import random

pygame.init()


WIDTH, HEIGHT = 600, 600
CELL = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

font = pygame.font.Font(None, 36)


snake = [(100, 100), (80, 100)]
dx, dy = CELL, 0
food = (300, 300)
score = 0
level = 1
speed = 10
alive = True

clock = pygame.time.Clock()

# тамақты қайта генерациялау (snake үстине түспеитин)
def spawn_food(snake):
    while True:
        x = random.randint(0, WIDTH // CELL - 1) * CELL
        y = random.randint(0, HEIGHT // CELL - 1) * CELL
        if (x, y) not in snake:
            return (x, y)

# теек бир бағытқа бұру (артқа кетпеу ушин)
def update_direction(event, dx, dy):
    if event.key == pygame.K_UP and dy == 0:
        return (0, -CELL)
    elif event.key == pygame.K_DOWN and dy == 0:
        return (0, CELL)
    elif event.key == pygame.K_LEFT and dx == 0:
        return (-CELL, 0)
    elif event.key == pygame.K_RIGHT and dx == 0:
        return (CELL, 0)
    return (dx, dy)


running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            dx, dy = update_direction(event, dx, dy)

    if alive:
        
        head = (snake[0][0] + dx, snake[0][1] + dy)

        # кабырғаға соғылса
        if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
            alive = False

        # Өзіне соғылса
        elif head in snake:
            alive = False
        else:
            snake.insert(0, head)

            # Food жегенде
            if head == food:
                score += 1
                food = spawn_food(snake)

                if score % 3 == 0:
                    level += 1
                    speed += 2
            else:
                snake.pop()

    
    for part in snake:
        pygame.draw.rect(screen, GREEN, (*part, CELL, CELL))

    
    pygame.draw.rect(screen, RED, (*food, CELL, CELL))

    # упаймен денгей
    info = font.render(f"Score: {score}   Level: {level}", True, WHITE)
    screen.blit(info, (10, 10))

    # если өлсе жазып шығару
    if not alive:
        game_over = font.render("Game Over!", True, RED)
        screen.blit(game_over, (WIDTH // 2 - 80, HEIGHT // 2 - 20))

    pygame.display.flip()
    clock.tick(speed)

pygame.quit()

