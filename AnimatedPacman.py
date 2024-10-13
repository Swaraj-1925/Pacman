import pygame
import math

def rotate_point(x, y, cx, cy, angle):

    s = math.sin(angle)
    c = math.cos(angle)
    x -= cx
    y -= cy
    new_x = x * c - y * s
    new_y = x * s + y * c
    return (new_x + cx, new_y + cy)

class Pacmanc(pygame.sprite.Sprite):
    change_x = 0
    change_y = 0
    
    def __init__(self, x, y, radius=13):
        pygame.sprite.Sprite.__init__(self)
   
        self.radius = radius
        self.mouth_angle = 0
        self.mouth_speed = 32
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = (x-6, y+12)  # Use center instead of topleft
        self.prev_x = x
        self.prev_y = y
        self.update_image()

    def update_image(self):
        self.image.fill((0, 0, 0, 0))
        center = self.radius, self.radius
        start_angle = self.mouth_angle / 2
        end_angle = 360 - self.mouth_angle / 2
        pygame.draw.arc(self.image, (255, 255, 0), self.image.get_rect(), 
                        math.radians(start_angle), math.radians(end_angle), self.radius)
        pygame.draw.circle(self.image, (255, 255, 0), center, self.radius)
        pygame.draw.polygon(self.image, (0, 0, 0), [
            center,
            rotate_point(self.radius * 2, self.radius, *center, math.radians(start_angle)),
            rotate_point(self.radius * 2, self.radius, *center, math.radians(end_angle))
        ])

    def prevdirection(self):
        self.prev_x = self.change_x
        self.prev_y = self.change_y

    def changespeed(self, x, y):
        self.change_x += x
        self.change_y += y
    
    def update_mouth_animation(self):
        if self.change_x != 0 or self.change_y != 0:  # Only animate when moving
            self.mouth_angle += self.mouth_speed
            if self.mouth_angle > 45 or self.mouth_angle < 0:
                self.mouth_speed = -self.mouth_speed
        self.update_image()

    def update(self, walls, gate):
        self.update_mouth_animation()
        
        old_center = self.rect.center
        new_center = (old_center[0] + self.change_x, old_center[1] + self.change_y)
        self.rect.center = new_center
        
        x_collide = pygame.sprite.spritecollide(self, walls, False)
        if x_collide:
            self.rect.centerx = old_center[0]
        
        y_collide = pygame.sprite.spritecollide(self, walls, False)
        if y_collide:
            self.rect.centery = old_center[1]

        if gate:
            gate_hit = pygame.sprite.spritecollide(self, gate, False)
            if gate_hit:
                self.rect.center = old_center

        # Rotate Pacman based on direction
        if self.change_x > 0:
            self.image = pygame.transform.rotate(self.image, 0)
        elif self.change_x < 0:
            self.image = pygame.transform.rotate(self.image, 180)
        elif self.change_y > 0:
            self.image = pygame.transform.rotate(self.image, 270)
        elif self.change_y < 0:
            self.image = pygame.transform.rotate(self.image, 90)
