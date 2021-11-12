import pygame


# Positions 
class Position():
    
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.isJump = False
        self.jumpCount = 10
         
    def jump(self):
        if self.isJump:
            if self.jumpCount >= -10:
                neg = 1
                if self.jumpCount < 0:
                    neg = -1
                self.y -= self.jumpCount**2 * 0.1 * neg
                self.jumpCount -= 1
            else:
                self.isJump = False
                self.jumpCount = 10    


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
        