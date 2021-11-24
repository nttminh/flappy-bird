import pygame
from pygame.sprite import Sprite


class Pillar(Sprite):
    """A Class to represent a pillar"""

    def __init__(self, fb_game, y, img_url):
        """Initialize the pillar and set its starting position."""
        super().__init__()
        self.fb_game = fb_game
        self.screen = fb_game.screen
        self.settings = fb_game.settings

        # Load the pillar image and set its rect attribute.
        self.image = pygame.image.load(img_url).convert_alpha()
        self.rect = self.image.get_rect(
            topleft=(self.fb_game.screen_width, y))

    def hit_left_border(self):
        """Return True if pillar is at left of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right <= screen_rect.left:
            return True

    def update(self):
        """Move the pillar to the left."""
        self.rect.x -= self.settings.pillar_speed

    def blitme(self):
        """Draw a pillar"""
        self.screen.blit(self.image, self.rect)
