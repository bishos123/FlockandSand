import pygame
import random
import tkinter as tk
from tkinter import ttk

# Configurações iniciais
width, height = 600, 400
flock = []

# Iniciando o Pygame
pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Inicializando valores padrão dos sliders
alignSlider_value = 1.5
cohesionSlider_value = 1.0
separationSlider_value = 2.0

class Boid:
    def __init__(self):
        self.position = pygame.Vector2(random.uniform(0, width), random.uniform(0, height))
        self.velocity = pygame.Vector2(random.uniform(-2, 2), random.uniform(-2, 2))
        self.acceleration = pygame.Vector2(0, 0)
        self.max_speed = 5
        self.max_force = 0.1

    def edges(self):
        self.position.x %= width
        self.position.y %= height

    def update(self):
        self.velocity += self.acceleration
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)
        self.position += self.velocity
        self.acceleration *= 0

    def apply_force(self, force):
        self.acceleration += force

    def flock(self, boids):
        alignment = self.align(boids) * alignSlider_value
        cohesion = self.cohere(boids) * cohesionSlider_value
        separation = self.separate(boids) * separationSlider_value
        self.apply_force(alignment)
        self.apply_force(cohesion)
        self.apply_force(separation)

    def align(self, boids):
        perception_radius = 50
        steering = pygame.Vector2(0, 0)
        total = 0
        for other in boids:
            if other != self and self.position.distance_to(other.position) < perception_radius:
                steering += other.velocity
                total += 1
        if total > 0:
            steering /= total
            steering.scale_to_length(self.max_speed)
            steering -= self.velocity
            steering.scale_to_length(self.max_force)
        return steering

    def cohere(self, boids):
        perception_radius = 50
        steering = pygame.Vector2(0, 0)
        total = 0
        for other in boids:
            if other != self and self.position.distance_to(other.position) < perception_radius:
                steering += other.position
                total += 1
        if total > 0:
            steering /= total
            steering -= self.position
            steering.scale_to_length(self.max_speed)
            steering -= self.velocity
            steering.scale_to_length(self.max_force)
        return steering

    def separate(self, boids):
        perception_radius = 30
        steering = pygame.Vector2(0, 0)
        total = 0
        for other in boids:
            distance = self.position.distance_to(other.position)
            if other != self and distance < perception_radius:
                diff = self.position - other.position
                diff /= distance  # Weight by distance
                steering += diff
                total += 1
        if total > 0:
            steering /= total
            steering.scale_to_length(self.max_speed)
            steering -= self.velocity
            steering.scale_to_length(self.max_force)
        return steering

    def show(self):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.position.x), int(self.position.y)), 3)

# Criar menos boids para teste de performance
for _ in range(100):
    flock.append(Boid())

# Função para atualizar valores dos sliders
def update_sliders():
    global alignSlider_value, cohesionSlider_value, separationSlider_value
    alignSlider_value = align_slider.get()
    cohesionSlider_value = cohesion_slider.get()
    separationSlider_value = separation_slider.get()

# Criar a janela Tkinter
root = tk.Tk()
root.title("Boid Simulation Controls")

# Sliders de alinhamento, coesão e separação
align_slider = ttk.Scale(root, from_=0, to=2, orient='horizontal', length=200, value=alignSlider_value, command=lambda val: update_sliders())
align_slider.pack(pady=10)
align_label = ttk.Label(root, text="Align Slider")
align_label.pack()

cohesion_slider = ttk.Scale(root, from_=0, to=2, orient='horizontal', length=200, value=cohesionSlider_value, command=lambda val: update_sliders())
cohesion_slider.pack(pady=10)
cohesion_label = ttk.Label(root, text="Cohesion Slider")
cohesion_label.pack()

separation_slider = ttk.Scale(root, from_=0, to=2, orient='horizontal', length=200, value=separationSlider_value, command=lambda val: update_sliders())
separation_slider.pack(pady=10)
separation_label = ttk.Label(root, text="Separation Slider")
separation_label.pack()

# Loop principal do Pygame e Tkinter
running = True
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for boid in flock:
        boid.edges()
        boid.flock(flock)
        boid.update()
        boid.show()

    pygame.display.flip()
    clock.tick(60)
    
    # Atualizar interface Tkinter
    root.update()

pygame.quit()
root.destroy()