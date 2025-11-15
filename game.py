"""Main game class managing state and game loop."""

import pygame
import sys
from constants import (
    SCREEN_SIZE, DARK_GREY, YELLOW,
    ENERGY_START, ENERGY_DECAY_MOVE, ENERGY_DECAY_VERTICAL,
    ENERGY_BURGER_BONUS, LIVES_START, SCREEN_TOTAL,
    BURGERS_REQUIRED, FINISH_X_THRESHOLD, FPS
)
from resources import load_image, load_sound
from player import Player


class Game:
    """Main game class managing state and game loop."""
    
    def __init__(self):
        # Initialize pygame
        pygame.init()
        pygame.font.init()
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.mixer.set_num_channels(64)
        
        # Create screens
        self.screen = pygame.Surface(SCREEN_SIZE)
        self.display_screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
        pygame.display.set_caption("The Bearded Ultra Runner")
        
        # Create font
        self.font = pygame.font.Font(pygame.font.get_default_font(), 24)
        self.clock = pygame.time.Clock()
        
        # Load resources
        self.background_image = load_image('Full-Background.png')
        self.burger_image = load_image('burger.png')
        self.rocks_image = load_image('Rock_Pile.png')
        self.finish_image = load_image('finish.png')
        self.heart_image = load_image('Heart.png')
        self.flask_image = load_image('flask.png')
        
        # Load and play music
        if load_sound('hold the line.ogg'):
            pygame.mixer.music.play(-1)
        
        # Initialize game state
        self.state = 'playing'
        self.player = Player()
        self.energy = ENERGY_START
        self.lives = LIVES_START
        self.screen_traveled = 0
        self.burger_collected = 0
        
        # Initialize game objects
        self.burgers = [
            pygame.Rect(220, 500, 32, 32),
            pygame.Rect(740, 350, 32, 32)
        ]
        self.rocks = [pygame.Rect(320, 550, 42, 42)]
        self.finish = pygame.Rect(808, 390, 262, 262)
        self.ground = pygame.Rect(0, 390, 1000, 290)
    
    def reset_player(self):
        """Reset player position and energy after losing a life."""
        self.player.reset()
        self.energy = ENERGY_START
    
    def handle_input(self):
        """Process all input events.
        
        Returns:
            bool: False if game should quit, True otherwise
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        
        if self.state == 'playing':
            keys = pygame.key.get_pressed()
            self.player.handle_input(keys)
            
            # Update energy based on movement
            if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
                self.energy -= ENERGY_DECAY_MOVE
            if keys[pygame.K_UP] or keys[pygame.K_DOWN]:
                self.energy -= ENERGY_DECAY_VERTICAL
        
        return True
    
    def update(self):
        """Update game state."""
        if self.state != 'playing':
            return
        
        # Update player
        self.player.update(SCREEN_SIZE[0])
        
        # Handle screen wrapping
        if self.player.x >= SCREEN_SIZE[0]:
            self.player.x = 0
            self.screen_traveled += 1
            # Refresh burgers if needed
            if not self.burgers:
                self.burgers = [
                    pygame.Rect(220, 500, 32, 32),
                    pygame.Rect(740, 350, 32, 32)
                ]
        
        # Check burger collection
        player_rect = self.player.get_rect()
        burgers_to_remove = []
        for burger in self.burgers:
            if burger.colliderect(player_rect):
                burgers_to_remove.append(burger)
                self.energy += ENERGY_BURGER_BONUS
                self.burger_collected += 1
        
        for burger in burgers_to_remove:
            self.burgers.remove(burger)
        
        # Check rock collisions
        for rock in self.rocks:
            if rock.colliderect(player_rect):
                self.lives -= 1
                self.reset_player()
                if self.lives <= 0:
                    self.state = 'lose'
                break
        
        # Check energy depletion
        if self.energy <= 0:
            self.lives -= 1
            self.reset_player()
            if self.lives <= 0:
                self.state = 'lose'
        
        # Check win condition
        in_final_screen = self.screen_traveled >= SCREEN_TOTAL
        if (in_final_screen and 
            self.burger_collected >= BURGERS_REQUIRED and 
            self.energy > 0 and 
            self.player.x >= FINISH_X_THRESHOLD):
            self.state = 'win'
    
    def draw_text(self, text, x, y):
        """Helper function to draw text on screen.
        
        Args:
            text: Text to display
            x: X coordinate
            y: Y coordinate
        """
        text_surface = self.font.render(text, True, YELLOW, DARK_GREY)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        self.screen.blit(text_surface, text_rect)
    
    def draw(self):
        """Draw everything on the screen."""
        # Background
        self.screen.fill(DARK_GREY)
        self.screen.blit(self.background_image, (0, 142))
        
        if self.state == 'playing':
            # Draw player
            self.player.draw(self.screen)
            
            # Draw burgers
            for burger in self.burgers:
                self.screen.blit(self.burger_image, (burger.x, burger.y))
            
            # Draw rocks
            for rock in self.rocks:
                self.screen.blit(self.rocks_image, (rock.x, rock.y))
            
            # Draw finish line
            if self.screen_traveled >= SCREEN_TOTAL:
                self.screen.blit(self.finish_image, (self.finish.x, self.finish.y))
            
            # Draw UI
            # Energy
            self.screen.blit(self.flask_image, (10, 10))
            self.draw_text(str(round(self.energy)), 50, 18)
            
            # Lives
            for i in range(self.lives):
                self.screen.blit(self.heart_image, (900 + (i * 30), 6))
        
        # Draw game over messages
        if self.state == 'lose':
            self.draw_text('You lost! DNF', 400, 250)
        elif self.state == 'win':
            self.draw_text('Congrats! You are a finisher!', 310, 250)
        
        # Scale and display
        scaled_screen = pygame.transform.smoothscale(
            self.screen, 
            self.display_screen.get_size()
        )
        self.display_screen.blit(scaled_screen, (0, 0))
        pygame.display.flip()
    
    def run(self):
        """Main game loop."""
        running = True
        while running:
            running = self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

