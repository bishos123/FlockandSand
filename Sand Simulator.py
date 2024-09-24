import pygame
import random

# Config inicial
w = 5  
cols = 120 
rows = 100 
hue_value = 200
gravity = 0.1


def make_2d_array(cols, rows, fill_value=0):
    return [[fill_value for _ in range(rows)] for _ in range(cols)]

def within_cols(i):
    return 0 <= i < cols

def within_rows(j):
    return 0 <= j < rows

# Pygame
pygame.init()
width, height = cols * w, rows * w
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

#  velocidade ++1
grid = make_2d_array(cols, rows)
velocity_grid = make_2d_array(cols, rows, 1)

# Fun DRAW
def draw_grid():
    global hue_value, grid, velocity_grid

    screen.fill((0, 0, 0))  

    
    if pygame.mouse.get_pressed()[0]:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_col = mouse_x // w
        mouse_row = mouse_y // w

        matrix = 5
        extent = matrix // 2
        for i in range(-extent, extent + 1):
            for j in range(-extent, extent + 1):
                if random.random() < 0.75:
                    col = mouse_col + i
                    row = mouse_row + j
                    if within_cols(col) and within_rows(row):
                        grid[col][row] = hue_value
                        velocity_grid[col][row] = 1
        hue_value += 0.5
        if hue_value > 360:
            hue_value = 1

    for i in range(cols):
        for j in range(rows):
            if grid[i][j] > 0:
                color = pygame.Color(0)
                color.hsva = (grid[i][j], 100, 100)
                x = i * w
                y = j * w
                pygame.draw.rect(screen, color, pygame.Rect(x, y, w, w))

    next_grid = make_2d_array(cols, rows)
    next_velocity_grid = make_2d_array(cols, rows)

    for i in range(cols):
        for j in range(rows):
            state = grid[i][j]
            velocity = velocity_grid[i][j]
            moved = False

            if state > 0:
                new_pos = int(j + velocity)
                for y in range(new_pos, j, -1):
                    below = grid[i][y] if within_rows(y) else -1
                    dir = 1 if random.random() < 0.5 else -1
                    below_a = grid[i + dir][y] if within_cols(i + dir) and within_rows(y) else -1
                    below_b = grid[i - dir][y] if within_cols(i - dir) and within_rows(y) else -1

                    if below == 0:
                        next_grid[i][y] = state
                        next_velocity_grid[i][y] = velocity + gravity
                        moved = True
                        break
                    elif below_a == 0:
                        next_grid[i + dir][y] = state
                        next_velocity_grid[i + dir][y] = velocity + gravity
                        moved = True
                        break
                    elif below_b == 0:
                        next_grid[i - dir][y] = state
                        next_velocity_grid[i - dir][y] = velocity + gravity
                        moved = True
                        break

            if state > 0 and not moved:
                next_grid[i][j] = state
                next_velocity_grid[i][j] = velocity + gravity

    grid = next_grid
    velocity_grid = next_velocity_grid

# Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_grid()
    pygame.display.flip()
    clock.tick(60)  # Limitar a 60 FPS

pygame.quit()