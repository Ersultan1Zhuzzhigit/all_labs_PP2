import pygame

screen = pygame.display.set_mode((600, 300))

pygame.display.set_caption("ERSS")

screen.fill((235, 64, 52))

runner = True
while runner:
    
    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runner = False
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                screen.fill((54, 62, 89))
            elif event.key == pygame.K_s:
                screen.fill((222, 221, 217))
    