import pygame

# Constant variables
SCREEN_SIZE = (1000,800)
DARK_GREY = (50,50,50)
# Initialize the game and screen
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Ultra running man")

# Game
running = True
while running:


    # Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw
    screen.fill(DARK_GREY)
    pygame.display.flip()


# Quit pygame
pygame.quit()