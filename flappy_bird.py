import pygame
import sys
import random

from settings import Settings
from bird import Bird
from pillar import Pillar


class FlappyBird:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.clock = pygame.time.Clock()
        self.screen_width = 400
        self.screen_height = 708

        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height))
        self.screen_width = self.screen.get_rect().width
        self.screen_height = self.screen.get_rect().height
        self.bg_image = pygame.image.load('images/background.bmp')
        self.game_over_surface = pygame.image.load(
            'images/gameover.png').convert_alpha()
        self.game_over_rect = self.game_over_surface.get_rect(
            center=(self.screen.get_rect().center))
        self.game_font = pygame.font.Font('fonts/04B_19.TTF', 40)

        # Game variables
        self.score = 0
        self.high_score = 0
        self.game_active = True
        self.SPAWNPIPE = pygame.USEREVENT
        pygame.time.set_timer(self.SPAWNPIPE, self.settings.spawn_cooldown)

        # Bird
        self.bird = Bird(self)
        self.bird_group = pygame.sprite.Group()
        self.bird_group.add(self.bird)

        # Pillar
        self.pillar_group = pygame.sprite.Group()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            if self.game_active is True:
                self._update_bird()
                self._update_pillar()
            self._update_screen()
            self.clock.tick(120)

    def _update_bird(self):
        """Check if bird collide with any objects"""
        self.bird_group.update()
        # If collide with pillars
        if pygame.sprite.spritecollideany(self.bird, self.pillar_group):
            self.game_active = False

        # If collide with windows border
        for bird in self.bird_group.sprites():
            if bird.is_touch_border():
                self.game_active = False

    def _create_pillar(self, y, gap, pillar_group):
        """Create two pillars and add it to the sprite"""
        pillar_group.add(Pillar(self, y-500, 'images/top.png'))
        pillar_group.add(Pillar(self, y + gap, 'images/bottom.png'))

    def _update_pillar(self):
        """Check if pillar goes out side left border"""
        self.pillar_group.update()
        for pillar in self.pillar_group:
            # Note that 2 pillars will hit left border at the same time
            if pillar.hit_left_border():
                self._increase_score()
                self.pillar_group.remove(pillar)

    def _increase_score(self):
        """
        Increase score, if score greater than high score, update high score
        """
        self.score += self.settings.score_step/2
        if self.score >= self.high_score:
            self.high_score = self.score

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        # Draw background
        self.screen.blit(self.bg_image, (0, 0))
        # Draw bird
        for bird in self.bird_group.sprites():
            bird.blitme()
        # Draw pillars
        for pillar in self.pillar_group.sprites():
            pillar.blitme()
        # Draw score
        self._display_score()
        # If game over
        if self.game_active is False:
            self.screen.blit(self.game_over_surface, self.game_over_rect)

        pygame.display.flip()

    def _display_score(self):
        """Display score to the screen"""
        score_surface = self.game_font.render(
            str(int(self.score)), True, 'aliceblue')
        score_rect = score_surface.get_rect(
            center=(self.screen_width/2, self.screen_height/8))

        if self.game_active:
            self.screen.blit(score_surface, score_rect)
        else:
            self.screen.blit(score_surface, score_rect)
            high_score_surface = self.game_font.render(
                f'High score: {int(self.high_score)}', True, 'aliceblue')
            high_score_rect = high_score_surface.get_rect(
                center=(
                    self.screen_width/2, self.screen_height*7/8
                ))
            self.screen.blit(high_score_surface, high_score_rect)

    def _restart_game(self):
        """Reset game to the original state"""
        self.game_active = True

        # Clear all the pillars in sprite
        for pillar in self.pillar_group:
            self.pillar_group.remove(pillar)

        # Reset the bird position and movement
        self.bird.rect.centery = self.screen.get_rect().centery
        self.bird.bird_movement = 0

        # Reset score
        self.score = 0

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._check_mouse_pressed_events(event)
            elif event.type == self.SPAWNPIPE:
                # Generate random y position of pillar
                range = self.screen_height - self.settings.gap
                y = random.randint(0, range)
                self._create_pillar(y, self.settings.gap, self.pillar_group)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_SPACE:
            self.bird.jump()
        if event.key == pygame.K_r and self.game_active is False:
            self._restart_game()
        if event.key == pygame.K_SPACE and self.game_active is False:
            self._restart_game()

    def _check_mouse_pressed_events(self, event):
        """Respond to mouse events."""
        mouse_presses = pygame.mouse.get_pressed()
        if mouse_presses[0]:
            self.bird.jump()
        if mouse_presses[0] and self.game_active is False:
            self._restart_game()


if __name__ == '__main__':
    """Make a game instance, and run the game."""
    fb = FlappyBird()
    fb.run_game()
