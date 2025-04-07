import pygame
import sys
import math

pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Paint')
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
gray = (200, 200, 200)

class Button:
    def __init__(self, x, y, width, height, text, color, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.action = action
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.Font(None, 30)
        text_surface = font.render(self.text, True, white)
        screen.blit(text_surface, (self.rect.x + 12, self.rect.y + 12))
    def check_action(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.action()

def set_black():
    global brush_color, mode
    brush_color = black
    mode = "brush"
def set_green():
    global brush_color, mode
    brush_color = green
    mode = "brush"
def set_red():
    global brush_color, mode
    brush_color = red
    mode = "brush"
def set_blue():
    global brush_color, mode
    brush_color = blue
    mode = "brush"
def clear_screen():
    screen.fill(white)
def exit_app():
    pygame.quit()
    sys.exit()
def set_brush():
    global mode
    mode = "brush"
def set_rect():
    global mode
    mode = "rect"
def set_circle():
    global mode
    mode = "circle"
def set_eraser():
    global mode
    mode = "eraser"
def set_square():
    global mode
    mode = "square"
def set_right_triangle():
    global mode
    mode = "r_triangle"
def set_equilateral_triangle():
    global mode
    mode = "e_triangle"
def set_rhombus():
    global mode
    mode = "rhombus"

drawing = False
brush_color = black
mode = "brush"
start_pos = None

buttons = [
    Button(10, 10, 60, 30, 'Black', black, set_black),
    Button(80, 10, 60, 30, 'Green', green, set_green),
    Button(150, 10, 60, 30, 'Red', red, set_red),
    Button(220, 10, 60, 30, 'Blue', blue, set_blue),
    Button(290, 10, 60, 30, 'Clear', gray, clear_screen),
    Button(360, 10, 60, 30, 'Exit', gray, exit_app),
    Button(430, 10, 60, 30, 'Brush', gray, set_brush),
    Button(500, 10, 60, 30, 'Rect', gray, set_rect),
    Button(570, 10, 60, 30, 'Circ', gray, set_circle),
    Button(640, 10, 60, 30, 'Eraser', gray, set_eraser),
    Button(10, 50, 80, 30, 'Square', gray, set_square),
    Button(100, 50, 120, 30, 'Right Tri', gray, set_right_triangle),
    Button(230, 50, 160, 30, 'Equi Triangle', gray, set_equilateral_triangle),
    Button(400, 50, 100, 30, 'Rhombus', gray, set_rhombus)
]

clear_screen()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and event.pos[1] > 90:
                if mode in ("rect", "circle", "square", "r_triangle", "e_triangle", "rhombus"):
                    start_pos = event.pos
                    drawing = True
                elif mode in ("brush", "eraser"):
                    drawing = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and event.pos[1] > 90:
                if mode in ("rect", "circle", "square", "r_triangle", "e_triangle", "rhombus") and drawing and start_pos:
                    end_pos = event.pos
                    if mode == "rect":
                        x = min(start_pos[0], end_pos[0])
                        y = min(start_pos[1], end_pos[1])
                        w = abs(end_pos[0] - start_pos[0])
                        h = abs(end_pos[1] - start_pos[1])
                        pygame.draw.rect(screen, brush_color, (x, y, w, h))
                    elif mode == "circle":
                        dx = end_pos[0] - start_pos[0]
                        dy = end_pos[1] - start_pos[1]
                        radius = int(math.hypot(dx, dy))
                        pygame.draw.circle(screen, brush_color, start_pos, radius)
                    elif mode == "square":
                        dx = end_pos[0] - start_pos[0]
                        dy = end_pos[1] - start_pos[1]
                        side = min(abs(dx), abs(dy))
                        x = start_pos[0] if dx >= 0 else start_pos[0] - side
                        y = start_pos[1] if dy >= 0 else start_pos[1] - side
                        pygame.draw.rect(screen, brush_color, (x, y, side, side))
                    elif mode == "r_triangle":
                        point1 = start_pos
                        point2 = (end_pos[0], start_pos[1])
                        point3 = (start_pos[0], end_pos[1])
                        pygame.draw.polygon(screen, brush_color, [point1, point2, point3])
                    elif mode == "e_triangle":
                        A = start_pos
                        B = end_pos
                        mid = ((A[0] + B[0]) / 2, (A[1] + B[1]) / 2)
                        base_length = math.hypot(B[0] - A[0], B[1] - A[1])
                        height_tri = (math.sqrt(3) / 2) * base_length
                        angle = math.atan2(B[1] - A[1], B[0] - A[0])
                        C = (mid[0] - height_tri * math.sin(angle), mid[1] + height_tri * math.cos(angle))
                        pygame.draw.polygon(screen, brush_color, [A, B, C])
                    elif mode == "rhombus":
                        x1, y1 = start_pos
                        x2, y2 = end_pos
                        top = ((x1 + x2) / 2, y1)
                        right = (x2, (y1 + y2) / 2)
                        bottom = ((x1 + x2) / 2, y2)
                        left = (x1, (y1 + y2) / 2)
                        pygame.draw.polygon(screen, brush_color, [top, right, bottom, left])
                    drawing = False
                    start_pos = None
                else:
                    drawing = False
        for button in buttons:
            button.check_action(event)
    if drawing and mode in ("brush", "eraser"):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_y > 90:
            color_to_use = brush_color if mode == "brush" else white
            pygame.draw.circle(screen, color_to_use, (mouse_x, mouse_y), 5)
    pygame.draw.rect(screen, gray, (0, 0, width, 90))
    for button in buttons:
        button.draw(screen)
    pygame.display.flip()