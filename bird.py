import pygame
from pygame.sprite import Sprite


class Bird(Sprite):
    def __init__(self, fb_game):
        """Initialize the bird and set its starting position."""
        super().__init__()
        self.screen = fb_game.screen
        self.screen_rect = fb_game.screen.get_rect()
        self.settings = fb_game.settings

        # Load the bird image and set its rect attribute.
        self.image = pygame.image.load('images/bird.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 30))
        self.rect = self.image.get_rect()

        # Movement
        self.bird_movement = 0

        # Start new bird near the middle left of the screen.
        self.rect.midleft = self.screen_rect.midleft
        self.rect.x = 50

    def blitme(self):
        """Draw the bird at its current location."""
        rotated_bird = self._rotate_bird()
        self.screen.blit(rotated_bird, self.rect)

    def update(self):
        """Update bird position"""
        self.bird_movement += self.settings.gravity
        self.rect.centery += self.bird_movement

    def jump(self):
        """Jump the bird"""
        self.bird_movement = 0
        self.bird_movement -= self.settings.jump_strength

    def _rotate_bird(self):
        """Create animation"""
        rotated_bird = pygame.transform.rotozoom(
            self.image, -self.bird_movement*3, 1)
        return rotated_bird

    def is_touch_border(self):
        """Check if touch the border"""
        if self.rect.top <= self.screen_rect.top:
            return True
        elif self.rect.bottom >= self.screen_rect.bottom:
            return True
        else:
            return False
