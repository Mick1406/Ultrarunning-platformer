"""Player class for managing player state, movement, and rendering."""

import pygame
import engine
from constants import (
    PLAYER_START_X, PLAYER_START_Y, PLAYER_WIDTH, PLAYER_HEIGHT,
    PLAYER_MOVE_SPEED, PLAYER_GROUND_Y
)
from resources import load_images


class Player:
    """Manages player state, movement, and rendering."""
    
    def __init__(self):
        self.x = PLAYER_START_X
        self.y = PLAYER_START_Y
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.speed = 0
        self.direction = 'right'
        self.state = 'idle'
        self.is_jumping = False
        self.jump_count = 0
        self.jump_height = 10
        self.on_ground = True
        
        # Load animations
        self.animations = {
            'idle': engine.Animation(load_images([
                'runner_00.png', 'runner_01.png', 'runner_02.png',
                'runner_03.png', 'runner_04.png'
            ])),
            'running': engine.Animation(load_images([
                'runner_08.png', 'runner_09.png', 'runner_10.png',
                'runner_11.png', 'runner_12.png', 'runner_13.png',
                'runner_14.png', 'runner_15.png'
            ])),
            'jumping': engine.Animation(load_images([
                'runner_16.png', 'runner_17.png', 'runner_18.png'
            ]))
        }
    
    def get_rect(self):
        """Get player's collision rectangle.
        
        Returns:
            pygame.Rect: Player's collision rectangle
        """
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def reset(self):
        """Reset player to starting position."""
        self.x = PLAYER_START_X
        self.y = PLAYER_START_Y
        self.speed = 0
        self.is_jumping = False
        self.jump_count = 0
        self.on_ground = True
        self.state = 'idle'
    
    def handle_input(self, keys):
        """Process player input and update state.
        
        Args:
            keys: pygame.key.get_pressed() result
        """
        moved = False
        
        if keys[pygame.K_LEFT]:
            self.x -= PLAYER_MOVE_SPEED
            self.direction = 'left'
            self.state = 'running'
            moved = True
        if keys[pygame.K_RIGHT]:
            self.x += PLAYER_MOVE_SPEED
            self.direction = 'right'
            self.state = 'running'
            moved = True
        
        if keys[pygame.K_SPACE] and self.on_ground and not self.is_jumping:
            self.is_jumping = True
            self.jump_count = self.jump_height
            self.on_ground = False
            self.state = 'jumping'
        
        if not moved and self.on_ground and not self.is_jumping:
            self.state = 'idle'
    
    def update(self, screen_width):
        """Update player position and physics.
        
        Args:
            screen_width: Width of the game screen
        """
        # Update animation
        self.animations[self.state].update()
        
        # Handle jumping
        if self.is_jumping:
            if self.jump_count >= -self.jump_height:
                neg = 1
                if self.jump_count < 0:
                    neg = -1
                self.y -= (self.jump_count ** 2) * 0.1 * neg
                self.jump_count -= 1
            else:
                self.is_jumping = False
                self.jump_count = 0
                self.y = PLAYER_GROUND_Y
                self.on_ground = True
                if self.state == 'jumping':
                    self.state = 'idle'
        
        # Keep player in bounds horizontally
        if self.x < 0:
            self.x = 0
        elif self.x > screen_width - self.width:
            self.x = screen_width - self.width
        
        # Keep player on ground when not jumping
        if not self.is_jumping and self.on_ground:
            self.y = PLAYER_GROUND_Y
    
    def draw(self, screen):
        """Draw the player on the screen.
        
        Args:
            screen: pygame.Surface to draw on
        """
        flip_x = (self.direction == 'left')
        self.animations[self.state].draw(screen, self.x, self.y, flip_x, False)

