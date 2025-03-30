import pygame
import random


pygame.init()


width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Racer Game")


gray = (100, 100, 100)
white = (255, 255, 255)
font = pygame.font.SysFont(None, 36)


car_img = pygame.image.load("car_Racer_images/Player.png")
car_img = pygame.transform.scale(car_img, (64, 100))

coin_img = pygame.image.load("car_Racer_images/coin.png")
coin_img = pygame.transform.scale(coin_img, (40, 40))

enemy_img = pygame.image.load("car_Racer_images/Enemy.png")
enemy_img = pygame.transform.scale(enemy_img, (64, 100))


car_x = width // 2
car_y = height - 120
car_speed = 5
car_width = 64

# Монетакоординаты мен жылдамдығы
coin_x = random.randint(50, width - 50)
coin_y = -50
coin_speed = 5


enemy_x = random.randint(50, width - 50)
enemy_y = -100
enemy_speed = 5

# очко,упай монета саны
score = 0


def draw_car(x, y):
    screen.blit(car_img, (x, y))


def draw_coin(x, y):
    screen.blit(coin_img, (x, y))


def draw_enemy(x, y):
    screen.blit(enemy_img, (x, y))

# Монетамен соқтығысты тексеру
def is_coin_collision(car_x, car_y, coin_x, coin_y):
    return abs(car_x - coin_x) < 50 and abs(car_y - coin_y) < 50

# карсы колик соқтығысты тексеру
def is_enemy_collision(car_x, car_y, enemy_x, enemy_y):
    return abs(car_x - enemy_x) < 50 and abs(car_y - enemy_y) < 80


running = True
clock = pygame.time.Clock()

while running:
    screen.fill(gray)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

   
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and car_x > 0:
        car_x -= car_speed
    if keys[pygame.K_RIGHT] and car_x < width - car_width:
        car_x += car_speed

   
    coin_y += coin_speed
    if coin_y > height:
        coin_x = random.randint(50, width - 50)
        coin_y = -50

    # Монета соқтығысы
    if is_coin_collision(car_x, car_y, coin_x, coin_y):
        score += 1
        coin_x = random.randint(50, width - 50)
        coin_y = -50

 
    enemy_y += enemy_speed
    if enemy_y > height:
        enemy_x = random.randint(50, width - 50)
        enemy_y = -100

    # карсы колик соқтығысы
    if is_enemy_collision(car_x, car_y, enemy_x, enemy_y):
        print("Game Over!")
        running = False

    
    draw_car(car_x, car_y)
    draw_coin(coin_x, coin_y)
    draw_enemy(enemy_x, enemy_y)

    # Ұпайды экранға шығару
    score_text = font.render(f"Coins: {score}", True, white)
    screen.blit(score_text, (10, 10))

    
    pygame.display.update()
    clock.tick(60)

pygame.quit()
