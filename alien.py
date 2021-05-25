import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""
    
    def __init__(self, Settings, screen):
        """Initialize the alien and set its starting position."""
        super(Alien, self).__init__()
        self.screen = screen
        self.Settings = Settings

    # Load the alien image and set its rect attribute.
        self.image = pygame.image.load('Images/Alien.jpg')
        self.rect = self.image.get_rect()

    # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

    def update(self):
        """Move the alien right or left."""
        self.x += (self.Settings.alien_speed_factor * self.Settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True