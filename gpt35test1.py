import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create a window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravity Simulation")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Particle class
class Particle:
    def __init__(self, x, y, radius, x_speed, y_speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.gravity_strength = 0.05  # Mild gravitational pull
        self.trail = []  # Trail for particles

    def apply_gravity(self):
        self.x_speed += random.uniform(-self.gravity_strength, self.gravity_strength)
        self.y_speed += random.uniform(-self.gravity_strength, self.gravity_strength)

    def move(self):
        self.x += self.x_speed
        self.y += self.y_speed

        # Add current position to the trail
        self.trail.append((self.x, self.y))

        # Limit the trail length to create a fading effect
        if len(self.trail) > 20:
            self.trail.pop(0)

    def draw_trail(self):
        for i in range(len(self.trail) - 1):
            pygame.draw.line(screen, self.color, self.trail[i], self.trail[i + 1], self.radius)

    def reset(self):
        self.trail = []

# Emitter class
class Emitter:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 10
        self.color = (255, 0, 0)
        self.emit_speed = 5  # Speed of emitted particles
        self.propelling_force = 0.05  # Weak propelling force

    def emit(self):
        angle = random.uniform(0, 2 * math.pi)
        x_speed = math.cos(angle) * (self.emit_speed + random.uniform(-self.propelling_force, self.propelling_force))
        y_speed = math.sin(angle) * (self.emit_speed + random.uniform(-self.propelling_force, self.propelling_force))
        return Particle(self.x, self.y, self.radius, x_speed, y_speed)

# Collector class
class Collector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 20
        self.color = (0, 0, 255)
        self.attract_force = 0.1  # Faint attraction force

    def attract(self, particle):
        dx = self.x - particle.x
        dy = self.y - particle.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance > 0:
            particle.x_speed += (dx / distance) * self.attract_force
            particle.y_speed += (dy / distance) * self.attract_force

# Initialize particles list
particles = []

# Create emitter and collector
emitter = Emitter(WIDTH // 4, HEIGHT // 2)
collector = Collector(3 * WIDTH // 4, HEIGHT // 2)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(WHITE)

    # Apply gravitational pull to particles and move them
    for particle in particles:
        particle.apply_gravity()
        particle.move()

        # Draw trails for particles
        particle.draw_trail()

    # Emit particles from the emitter
    if len(particles) < 100:
        new_particle = emitter.emit()
        particles.append(new_particle)

    # Attract particles towards the collector
    for particle in particles:
        collector.attract(particle)

    # Reset the simulation when 'R' key is pressed
    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
        particles = []  # Clear all particles

    # Update the display
    pygame.display.flip()
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
