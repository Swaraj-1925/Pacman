import pygame
from Algo import bresenham_circle
from Constant import white,red
# It derives from the "Sprite" class in Pygame
class Block(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self) 
 
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(white)
        self.image.set_colorkey(white)
        #pygame.draw.ellipse(self.image,color,[0,0,width,height])
        bresenham_circle(self.image, width//2, height//2, min(width, height)//2 - 1,color)
        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values 
        # of rect.x and rect.y
        self.rect = self.image.get_rect() 
