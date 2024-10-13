import pygame
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pacman")

# Colors
BLACK = (0, 0, 0)

# FPS (Frames per second)
FPS = 60
clock = pygame.time.Clock()

# Function to rotate points
def rotate_point(x, y, cx, cy, angle):
    s = math.sin(angle)
    c = math.cos(angle)
    x -= cx
    y -= cy
    new_x = x * c - y * s
    new_y = x * s + y * c
    return (new_x + cx, new_y + cy)

# Pacman class definition
class Pacman(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        super().__init__()
        self.radius = radius
        self.mouth_angle = 0
        self.mouth_speed = 0.5
        self.image = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        self.update_image()

    def update_image(self):
        self.image.fill((0, 0, 0, 0))
        center = self.radius, self.radius
        start_angle = self.mouth_angle / 2
        end_angle = 360 - self.mouth_angle / 2
        pygame.draw.arc(self.image, (255, 255, 0), self.image.get_rect(), 
                        math.radians(start_angle), math.radians(end_angle), self.radius)
        pygame.draw.line(self.image, (255, 255, 0), center, 
                         rotate_point(self.radius*2, self.radius, *center, math.radians(start_angle)))
        pygame.draw.line(self.image, (255, 255, 0), center, 
                         rotate_point(self.radius*2, self.radius, *center, math.radians(end_angle)))

    def update(self):
        self.mouth_angle += self.mouth_speed
        if self.mouth_angle > 45 or self.mouth_angle < 0:
            self.mouth_speed = -self.mouth_speed
        self.update_image()

# Create a sprite group and add Pacman
all_sprites = pygame.sprite.Group()
pacman = Pacman(300, 300, 50)  # Adjusted radius for visibility
all_sprites.add(pacman)

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the game state
    all_sprites.update()

    # Clear the screen
    screen.fill(BLACK)

    # Draw everything
    all_sprites.draw(screen)

    # Refresh the display
    pygame.display.flip()

    # Maintain FPS
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
