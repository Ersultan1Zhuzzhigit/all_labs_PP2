import pygame
import sys
import random

pygame.init()
width, height = 500, 500
cell_size = 10
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Simple Snake with Levels')
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
white = (255, 255, 255)
snake_pos = [100, 100]
snake_body = [[100, 100], [90, 100], [80, 100]]
direction = 'RIGHT'
change_to = direction
score = 0
level = 1
foods_eaten = 0
speed = 10
clock = pygame.time.Clock()
food_lifetime = 5000

def generate_food():
    x = random.randrange(cell_size, width - cell_size, cell_size)
    y = random.randrange(cell_size, height - cell_size, cell_size)
    while [x, y] in snake_body:
        x = random.randrange(cell_size, width - cell_size, cell_size)
        y = random.randrange(cell_size, height - cell_size, cell_size)
    weight = random.randint(1, 5)
    spawn_time = pygame.time.get_ticks()
    return {"pos": [x, y], "weight": weight, "spawn_time": spawn_time}

food = generate_food()
game_over = False

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'DOWN':
                change_to = 'UP'
            elif event.key == pygame.K_DOWN and direction != 'UP':
                change_to = 'DOWN'
            elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                change_to = 'LEFT'
            elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                change_to = 'RIGHT'
    direction = change_to
    if direction == 'UP':
        snake_pos[1] -= cell_size
    elif direction == 'DOWN':
        snake_pos[1] += cell_size
    elif direction == 'LEFT':
        snake_pos[0] -= cell_size
    elif direction == 'RIGHT':
        snake_pos[0] += cell_size
    if snake_pos[0] < 0 or snake_pos[0] >= width or snake_pos[1] < 0 or snake_pos[1] >= height:
        game_over = True
    snake_body.insert(0, list(snake_pos))
    if snake_pos == food["pos"]:
        score += food["weight"]
        foods_eaten += 1
        if foods_eaten % 3 == 0:
            level += 1
            speed += 2
        food = generate_food()
    else:
        snake_body.pop()
    if snake_pos in snake_body[1:]:
        game_over = True
    current_time = pygame.time.get_ticks()
    if current_time - food["spawn_time"] > food_lifetime:
        food = generate_food()
    screen.fill(black)
    for block in snake_body:
        pygame.draw.rect(screen, green, pygame.Rect(block[0], block[1], cell_size, cell_size))
    pygame.draw.rect(screen, red, pygame.Rect(food["pos"][0], food["pos"][1], cell_size, cell_size))
    font = pygame.font.SysFont('arial', 20)
    weight_text = font.render(str(food["weight"]), True, white)
    screen.blit(weight_text, (food["pos"][0], food["pos"][1]))
    score_text = font.render("Score: " + str(score), True, white)
    level_text = font.render("Level: " + str(level), True, white)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 30))
    pygame.display.flip()
    clock.tick(speed)

pygame.quit()
sys.exit()