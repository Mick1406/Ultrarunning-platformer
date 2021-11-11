import pygame


# Positions 
class Position():
    
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)

# Animations
class Animations():
    
    def __init__(self):
        self.animationList = {}
        
    def add(self, state, animation):
            self.animationList[state] = animation


class Animation():
    
    def __init__(self, imageList):
        self.imageList = imageList
        self.imageIndex = 0
        self.animationTimer = 0
        self.animationSpeed = 10
        
    def update(self):
        self.animationTimer += 1
        if self.animationTimer >= self.animationSpeed:
            self.animationTimer = 0
            self.imageIndex += 1
            if self.imageIndex > len(self.imageList) - 1:
                self.imageIndex = 0
    
    def draw(self, screen, x, y, flipX, flipY ):
        screen.blit(pygame.transform.flip(self.imageList[self.imageIndex], flipX, flipY), (x,y))
        
        
# Entities
class Entity():
    
    def __init__(self):
        self.state = 'idle'
        self.position = None
        self.animations = None
        