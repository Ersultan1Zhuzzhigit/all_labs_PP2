import pygame

pygame.init()


WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")


canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill((255, 255, 255))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)


colors = [BLACK, RED, BLUE, GREEN, YELLOW, PURPLE, ORANGE, CYAN]
color = BLACK 

drawing = False 
start_pos = None 
radius = 5  
running = True
mode = "brush" 

while running:
    screen.blit(canvas, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

       
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                mode = "rectangle" 
            if event.key == pygame.K_c:
                mode = "circle" 
            if event.key == pygame.K_b:
                mode = "brush"
            if event.key == pygame.K_e:
                mode = "eraser" 

            if pygame.K_1 <= event.key <= pygame.K_8:
                color = colors[event.key - pygame.K_1]

            
            if event.key == pygame.K_DOWN and radius > 3:
                radius -= 2
            if event.key == pygame.K_UP and radius < 30:
                radius += 2

        
        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos  

        
        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            end_pos = event.pos
            if mode == "rectangle":
                x1, y1 = start_pos
                x2, y2 = end_pos
                pygame.draw.rect(canvas, color, (min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1)), 2)
            if mode == "circle":
                x1, y1 = start_pos
                x2, y2 = end_pos
                radius = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5) // 2
                center = ((x1 + x2) // 2, (y1 + y2) // 2)
                pygame.draw.circle(canvas, color, center, radius, 2)

        
        if event.type == pygame.MOUSEMOTION and drawing:
            if mode == "brush":
                pygame.draw.line(canvas, color, start_pos, event.pos, radius)
                start_pos = event.pos
            elif mode == "eraser":
                pygame.draw.line(canvas, WHITE, start_pos, event.pos, radius)
                start_pos = event.pos

            
            elif mode in ["rectangle", "circle"]:
                screen.blit(canvas, (0, 0))
                x1, y1 = start_pos
                x2, y2 = event.pos

                if mode == "rectangle":
                    pygame.draw.rect(screen, color, (min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1)), 2)
                elif mode == "circle":
                    radius = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5) // 2
                    center = ((x1 + x2) // 2, (y1 + y2) // 2)
                    pygame.draw.circle(screen, color, center, radius, 2)

    pygame.display.update()

pygame.quit()