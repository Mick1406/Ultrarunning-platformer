"""Resource loading utilities with error handling."""

import os
import pygame
from constants import IMAGE_DIR, SOUND_DIR


def load_image(filename, directory=IMAGE_DIR):
    """Safely load an image file with error handling.
    
    Args:
        filename: Name of the image file
        directory: Directory containing the image (default: IMAGE_DIR)
    
    Returns:
        pygame.Surface: The loaded image, or a placeholder surface if loading fails
    """
    path = os.path.join(directory, filename)
    try:
        image = pygame.image.load(path)
        return image
    except pygame.error as e:
        print(f"Error loading image {path}: {e}")
        # Return a placeholder surface if image fails to load
        return pygame.Surface((32, 32))


def load_images(filenames, directory=IMAGE_DIR):
    """Load multiple image files.
    
    Args:
        filenames: List of image filenames
        directory: Directory containing the images (default: IMAGE_DIR)
    
    Returns:
        list: List of pygame.Surface objects
    """
    return [load_image(f, directory) for f in filenames]


def load_sound(filename, directory=SOUND_DIR):
    """Safely load a sound file with error handling.
    
    Args:
        filename: Name of the sound file
        directory: Directory containing the sound (default: SOUND_DIR)
    
    Returns:
        bool: True if sound loaded successfully, False otherwise
    """
    path = os.path.join(directory, filename)
    try:
        pygame.mixer.music.load(path)
        return True
    except pygame.error as e:
        print(f"Error loading sound {path}: {e}")
        return False

