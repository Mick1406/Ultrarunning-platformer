import pygame

# Constant variables
SCREEN_SIZE = (1000,800)
DARK_GREY = (50,50,50)
# Initialize the game and screen
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Ultra running man")

# Background
background_image = pygame.image.load('images/Full-Background.png')

# Player
player_image = pygame.image.load('images/runner_00.png')

# Game
running = True
while running:


    # Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw
    screen.fill(DARK_GREY)
    screen.blit(background_image, (0,142))
    screen.blit(player_image, (20,500))
    pygame.display.flip()


# Quit pygame
pygame.quit()