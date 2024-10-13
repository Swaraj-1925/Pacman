import pygame
import math

class Player(pygame.sprite.Sprite):
    change_x = 0
    change_y = 0
    
    def __init__(self, x, y, filename):
        pygame.sprite.Sprite.__init__(self)
   
        self.original_image = pygame.image.load(filename).convert_alpha()
        self.image = self.original_image.copy()
  
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x
        self.prev_x = x
        self.prev_y = y

        self.angle = 0
        self.mouth_speed = 5
        self.mouth_open = False

    def prevdirection(self):
        self.prev_x = self.change_x
        self.prev_y = self.change_y

    def changespeed(self, x, y):
        self.change_x += x
        self.change_y += y
    
    def update_mouth_animation(self):
        if self.change_x != 0 or self.change_y != 0:  # Only animate when moving
            if self.mouth_open:
                self.angle += self.mouth_speed
                if self.angle >= 45:
                    self.mouth_open = False
            else:
                self.angle -= self.mouth_speed
                if self.angle <= 0:
                    self.mouth_open = True
        
        center = self.rect.center
        self.image = self.original_image.copy()
        
        # Create a mask surface
        mask = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
        pygame.draw.arc(mask, (255, 255, 255, 255), self.image.get_rect(), 
                        math.radians(self.angle), math.radians(360 - self.angle))
        
        # Apply the mask to the image
        self.image.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        
        # Ensure the image is not completely transparent
        if self.image.get_at((self.image.get_width() // 2, self.image.get_height() // 2))[3] == 0:
            self.image = self.original_image.copy()
        
        self.rect = self.image.get_rect(center=center)

    def update(self, walls, gate):
        self.update_mouth_animation()
        
        old_x = self.rect.left
        new_x = old_x + self.change_x
        self.rect.left = new_x
        
        old_y = self.rect.top
        new_y = old_y + self.change_y

        x_collide = pygame.sprite.spritecollide(self, walls, False)
        if x_collide:
            self.rect.left = old_x
        else:
            self.rect.top = new_y
            y_collide = pygame.sprite.spritecollide(self, walls, False)
            if y_collide:
                self.rect.top = old_y

        if gate:
            gate_hit = pygame.sprite.spritecollide(self, gate, False)
            if gate_hit:
                self.rect.left = old_x
                self.rect.top = old_y
