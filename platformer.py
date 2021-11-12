import pygame
import engine

# Helper functions 
def drawText(t, x, y):
    text = font.render(t, True, YELLOW, DARK_GREY )
    text_rectangle = text.get_rect()
    text_rectangle.topleft = (x,y)
    screen.blit(text, text_rectangle) 

# Constant variables
SCREEN_SIZE = (1000,800)
DARK_GREY = (50,50,50)
YELLOW = (255,204,0)

# Initialize the game
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("The Bearded Ultra Runner")
clock = pygame.time.Clock()
font = pygame.font.Font(pygame.font.get_default_font(), 24)

# Game states (playing / winning / losing)
game_state = 'playing'

# Set entities
entities = []

# Background
background_image = pygame.image.load('images/Full-Background.png')

# Player parameters
player_image = pygame.image.load('images/runner_01.png')
player_x = 20
player_y = 500
player_width = 52
player_height = 72
player_speed = 0
player_acceleration = 0.1
player_direction = 'right' # or 'left'
player_state = 'idle' # or 'running' or jumping
player_animations = {'idle': engine.Animation([
                        pygame.image.load('images/runner_00.png'),
                        pygame.image.load('images/runner_01.png'),
                        pygame.image.load('images/runner_02.png'),
                        pygame.image.load('images/runner_03.png'),
                        pygame.image.load('images/runner_04.png')
                     ]),
                     'running': engine.Animation([
                         pygame.image.load('images/runner_08.png'),
                         pygame.image.load('images/runner_09.png'),
                         pygame.image.load('images/runner_10.png'),
                         pygame.image.load('images/runner_11.png'),
                         pygame.image.load('images/runner_12.png'),
                         pygame.image.load('images/runner_13.png'),
                         pygame.image.load('images/runner_14.png'),
                         pygame.image.load('images/runner_15.png'),
                     ]),
                     'jumping': engine.Animation([
                         pygame.image.load('images/runner_16.png'),
                         pygame.image.load('images/runner_17.png'),
                         pygame.image.load('images/runner_18.png')
                     ])
                     }

# Burgers
burger_image = pygame.image.load('images/burger.png')
burgers = [pygame.Rect(220, 500, 32, 32), pygame.Rect(740, 350, 32, 32)]
burger_collected = 0

# burger1 = engine.Entity()
# burger1.position = engine.Position(220, 500, 32, 32)

# burger2 = engine.Entity()
# burger2.position = engine.Position(740, 350, 32, 32)

# entities.append(burger1)
# entities.append(burger2)


# Rocks
rocks_image = pygame.image.load('images/Rock_Pile.png')
rocks = [pygame.Rect(320, 550, 42, 42)]

# Finish line
finish_image = pygame.image.load('images/finish.png')
finish = [pygame.Rect(808, 390, 262, 262)]

# Energy score and number of lives
energy = 10 
lives = 3
heart_image = pygame.image.load('images/Heart.png')

# Flask of water
flask_image = pygame.image.load('images/flask.png')

# Platform (ground for running) - matching background platform
ground = [pygame.Rect(0, 390, 1000, 290)]

# Load and play uusic of the game
pygame.mixer.music.load('sounds/hold the line.ogg')
pygame.mixer.music.play(-1)

#-----------------------------------------------------------
# Start the game loop
#-----------------------------------------------------------
running = True
while running:

    #----------------------------------------------------------------
    # Input
    #----------------------------------------------------------------

    # Check for quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    if game_state == 'playing':
        # Update player position
        new_player_x = player_x
        new_player_y = player_y

        # Player input event - move the runner
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            new_player_x -= 3
            energy -= 0.017
            player_direction = 'left'
            player_state = 'running'
        if keys[pygame.K_RIGHT]:
            new_player_x += 3
            energy -= 0.017
            player_direction = 'right'
            player_state = 'running'
        if keys[pygame.K_UP]:
            new_player_y -= 1
            energy -= 0.01
            player_speed += player_acceleration
        if keys[pygame.K_DOWN]:
            new_player_y += 2
            energy -= 0.01
            player_speed -= player_acceleration
        if not keys[pygame.K_DOWN] and keys[pygame.K_UP] and keys[pygame.K_RIGHT] and keys[pygame.K_LEFT]:
            player_state = 'idle'
            
        # Jumps
        if keys[pygame.K_SPACE]:
            player_state = 'jumping'
            engine.Position.isJump = True
   
    #----------------------------------------------------------------
    # Update
    #----------------------------------------------------------------

    if game_state == 'playing':
        
        # Update player Animation
        player_animations[player_state].update()
        
        # Horizontal movement / position not out of bounds
        # if in bounds
        if new_player_x >= 0 and new_player_x <=1000:
            player_x = new_player_x
        else:
            player_x == 0

        # Vertical movement 
        player_speed += player_acceleration
        #new_player_y +=  player_speed

        if new_player_y != player_y and new_player_y >= 0 and new_player_y <= 800:
            player_y = new_player_y #- player_speed
            new_player_y == 500
        else:
            player_y == 500


        # Collect burgers
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        for b in burgers:
            if b.colliderect(player_rect):
                burgers.remove(b)
                energy += 2
                burger_collected += 1
                # interim (see how energy stores are changing)
                print(energy)
                # Change the game state if no lives remaining
        
        if burger_collected >= 2 and energy>0 and player_x >= 880:
            game_state = 'win'

        # Hit obstacles
        for r in rocks:
            if r.colliderect(player_rect):
                lives -= 1
                # Reset player position and energy after losing a life
                player_x = 20
                player_y = 500
                player_speed = 0
                energy = 10
                # Change the game state if no lives remaining
                if lives <= 0:
                    game_state = 'lose'

        # Run out of energy 
        if energy <= 0:
            lives -= 1
            # Reset player position and energy after losing a life
            player_x = 20
            player_y = 500
            player_speed = 0
            energy = 10
            # Change the game state if no lives remaining
            if lives <= 0:
                game_state = 'lose'


    #----------------------------------------------------------------
    # Draw
    #----------------------------------------------------------------

    # Background
    screen.fill(DARK_GREY)
    screen.blit(background_image, (0,142))
    
    if game_state == 'playing':

        # Player
        if player_direction == 'right':
            # screen.blit(player_image, (player_x,player_y))
            player_animations[player_state].draw(screen, player_x, player_y, False, False)
        elif player_direction == 'left':
            # screen.blit(pygame.transform.flip(player_image, True, False), (player_x,player_y))
            player_animations[player_state].draw(screen, player_x, player_y, True, False)
            
        # Burgers
        for b in burgers:
            screen.blit(burger_image, (b[0], b[1]))

        # for entity in entities:
        #     if entity.position is not None:
        #         screen.blit(burger_image, (entity.position.rect.x, entity.position.rect.y))
        
        # Rocks
        for r in rocks:
            screen.blit(rocks_image, (r[0], r[1]))

        # Player information display
        # Energy left
        screen.blit(flask_image, (10,10))
        drawText(str(round(energy)), 50, 18)

        # Lives
        for l in range(lives):
            screen.blit(heart_image, (900 + (l*30), 6))


        # Finish License
        screen.blit(finish_image, (finish[0][0],finish[0][1]))
        
    # Display game status when either finished or no more lives
    if game_state == 'lose':
        drawText('You lost! DNF', 400, 250)
    elif game_state == 'win':
        drawText('Congrats! You are a finisher!', 310, 250)


    # Present screen
    pygame.display.flip()

    clock.tick(60)


# Quit pygame
pygame.quit()