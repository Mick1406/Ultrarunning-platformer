import pygame

# Constant variables
SCREEN_SIZE = (1000,800)
DARK_GREY = (50,50,50)

# Initialize the game
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Ultra running man")
clock = pygame.time.Clock()

# Background
background_image = pygame.image.load('images/Full-Background.png')

# Player parameters
player_image = pygame.image.load('images/runner_00.png')
player_x = 20
player_y = 500
player_speed = 0
player_acceleration = 0.1

# Burgers


# Start the game loop
running = True
while running:

    #----------------------------------------------------------------
    # Input
    #----------------------------------------------------------------
    
    # Check for quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update player position
    new_player_x = player_x
    new_player_y = player_y

    # Player input event - move the runner
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        new_player_x -= 2
    if keys[pygame.K_RIGHT]:
        new_player_x += 2
    if keys[pygame.K_UP]:
        new_player_y -= 1
        player_speed += player_acceleration
    if keys[pygame.K_DOWN]:
        new_player_y += 2
        player_speed -= player_acceleration
   

    # Horizontal movement / position not out of bounds
    # if in bounds
    if new_player_x >= 0 and new_player_x <=1000:
        player_x = new_player_x
    else:
        player_x == 0

    # Vertical movement 
    player_speed += player_acceleration
    # new_player_y +=  player_speed

    if new_player_y != player_y and new_player_y >= 0 and new_player_y <= 800:
        player_y = new_player_y #- player_speed
        new_player_y == 500
    else:
        player_y == 500

    # Draw
    screen.fill(DARK_GREY)
    screen.blit(background_image, (0,142))
    screen.blit(player_image, (player_x,player_y))
    pygame.display.flip()

    clock.tick(60)

# Quit pygame
pygame.quit()