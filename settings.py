import pygame


class Settings:
    """Settings class includes all the settings that were used in game"""

    def __init__(self):
        """Initialize the game's settings."""
        # You can change the background of your desire
        self.bg_image = pygame.image.load('images/background.bmp')
        self.score_step = 1

        # Bird
        self.gravity = 0.20
        self.jump_strength = 9

        # Pillar
        self.pillar_speed = 5
        self.gap = 400
        self.spawn_cooldown = 200
