import pygame
import random

# Making canvas
screen = pygame.display.set_mode((900, 700))
screen.fill((255, 255, 255))

# Setting Title
pygame.display.set_caption('Paint(2.0)')

draw_on = False
last_pos = (0, 0)

# Radius of the Brush
radius = 5

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 128, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
PINK = (255, 192, 203)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
BROWN = (139, 69, 19)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

# Menu
pygame.draw.rect(screen, RED, (0, 50, 20, 20))
pygame.draw.rect(screen, ORANGE, (0, 70, 20, 20))
pygame.draw.rect(screen, YELLOW, (0, 90, 20, 20))
pygame.draw.rect(screen, GREEN, (0, 110, 20, 20))
pygame.draw.rect(screen, BLUE, (0, 130, 20, 20))
pygame.draw.rect(screen, PURPLE, (0, 150, 20, 20))
pygame.draw.rect(screen, PINK, (0, 170, 20, 20))
pygame.draw.rect(screen, BLACK, (0, 190, 20, 20))
pygame.draw.rect(screen, GRAY, (0, 210, 20, 20))
pygame.draw.rect(screen, BROWN, (0, 230, 20, 20))
pygame.draw.rect(screen, CYAN, (0, 250, 20, 20))
pygame.draw.rect(screen, MAGENTA, (0, 270, 20, 20))

eraser = pygame.transform.scale(pygame.image.load("eraser.png"), (40, 40))
screen.blit(eraser, [0, 290])

def roundline(canvas, color, start, end, radius=1):
    Xaxis = end[0] - start[0]
    Yaxis = end[1] - start[1]
    dist = max(abs(Xaxis), abs(Yaxis))
    for i in range(dist):
        x = int(start[0] + float(i) / dist * Xaxis)
        y = int(start[1] + float(i) / dist * Yaxis)
        pygame.draw.circle(canvas, color, (x, y), radius)

try:
    while True:
        e = pygame.event.wait()

        if e.type == pygame.QUIT:
            raise StopIteration

        if e.type == pygame.MOUSEBUTTONDOWN:
            spot = pygame.mouse.get_pos()
            # Selecting Color Code
            if spot[0] < 20 and 50 < spot[1] < 70:
                color = RED
            elif spot[0] < 20 and 70 < spot[1] < 90:
                color = ORANGE
            elif spot[0] < 20 and 90 < spot[1] < 110:
                color = YELLOW
            elif spot[0] < 20 and 110 < spot[1] < 130:
                color = GREEN
            elif spot[0] < 20 and 130 < spot[1] < 150:
                color = BLUE
            elif spot[0] < 20 and 150 < spot[1] < 170:
                color = PURPLE
            elif spot[0] < 20 and 170 < spot[1] < 190:
                color = PINK
            elif spot[0] < 20 and 190 < spot[1] < 210:
                color = BLACK
            elif spot[0] < 20 and 210 < spot[1] < 230:
                color = GRAY
            elif spot[0] < 20 and 230 < spot[1] < 250:
                color = BROWN
            elif spot[0] < 20 and 250 < spot[1] < 270:
                color = CYAN
            elif spot[0] < 20 and 270 < spot[1] < 290:
                color = MAGENTA
            elif 0 < spot[0] < 40 and 290 < spot[1] < 330:
                color = WHITE
            if spot[0] > 60:
                pygame.draw.circle(screen, color, e.pos, radius)
            draw_on = True
        # When mouse button released it will stop drawing
        if e.type == pygame.MOUSEBUTTONUP:
            draw_on = False
        # It will draw a continuous circle with the help of roundline function.
        if e.type == pygame.MOUSEMOTION:
            spot = pygame.mouse.get_pos()
            if draw_on and spot[0] > 60:
                pygame.draw.circle(screen, color, e.pos, radius)
                roundline(screen, color, e.pos, last_pos, radius)
            last_pos = e.pos

        if e.type == pygame.KEYDOWN:
            spot = pygame.mouse.get_pos()
            if e.key == pygame.K_r:
                rect_size = 100  # Set the size of the square
                pygame.draw.rect(screen, color, (spot[0], spot[1], rect_size, rect_size))
            elif e.key == pygame.K_c:
                circle_radius = 50  # Set the radius of the circle
                pygame.draw.circle(screen, color, (spot[0], spot[1]), circle_radius)

        pygame.display.flip()

except StopIteration:
    pass

# Quit
pygame.quit()
