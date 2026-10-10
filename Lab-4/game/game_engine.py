import array
import math

import pygame
from .snake import Snake
from .food import Food

# Game Engine

WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (220, 60, 60)
BLACK = (0, 0, 0)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cell_size = 20
        self.grid_width = width // self.cell_size
        self.grid_height = height // self.cell_size

        self.snake = Snake(self.grid_width // 2, self.grid_height // 2, self.cell_size)
        self.food = Food(self.grid_width, self.grid_height, self.cell_size)

        self.score = 0
        self.font = pygame.font.SysFont("Arial", 30)
        self.title_font = pygame.font.SysFont("Arial", 48, bold=True)

        self.moves_per_second = 8
        self._frame_counter = 0

        self.game_over = False
        self._game_over_logged = False

        self.eat_sound = self._create_tone_sound(660, 0.08, 0.32)
        self.game_over_sound = self._create_tone_sound(180, 0.22, 0.35)

    def _create_tone_sound(self, frequency, duration, volume):
        if not pygame.mixer.get_init():
            return None

        sample_rate = 22050
        total_samples = int(sample_rate * duration)
        samples = array.array('h')

        for i in range(total_samples):
            elapsed = i / sample_rate
            amplitude = math.sin(2 * math.pi * frequency * elapsed)
            samples.append(int(32767 * volume * amplitude))

        try:
            return pygame.mixer.Sound(buffer=samples.tobytes())
        except Exception:
            return None

    def _play_sound(self, sound):
        if sound is None:
            return

        try:
            sound.play()
        except Exception:
            pass

    def _start_game(self, moves_per_second):
        self.moves_per_second = moves_per_second
        self.snake = Snake(self.grid_width // 2, self.grid_height // 2, self.cell_size)
        self.food = Food(self.grid_width, self.grid_height, self.cell_size)
        self.score = 0
        self._frame_counter = 0
        self.game_over = False
        self._game_over_logged = False

    def _handle_game_over_choice(self, choice):
        if choice in (pygame.K_1, pygame.K_e):
            self._start_game(6)
            return
        if choice in (pygame.K_2, pygame.K_m):
            self._start_game(8)
            return
        if choice in (pygame.K_3, pygame.K_h):
            self._start_game(10)
            return
        if choice in (pygame.K_4, pygame.K_x):
            pygame.quit()
            raise SystemExit

    def handle_keydown(self, key):
        if self.game_over:
            self._handle_game_over_choice(key)
            return

        # Direction changes are applied immediately on key press.
        if key in (pygame.K_UP, pygame.K_w):
            self.snake.set_direction(0, -1)
        elif key in (pygame.K_DOWN, pygame.K_s):
            self.snake.set_direction(0, 1)
        elif key in (pygame.K_LEFT, pygame.K_a):
            self.snake.set_direction(-1, 0)
        elif key in (pygame.K_RIGHT, pygame.K_d):
            self.snake.set_direction(1, 0)

    def handle_input(self):
        # Reserved for continuously-held-key input (not used for a
        # grid-based snake, but kept here to mirror the engine's shape).
        pass

    def update(self):
        if self.game_over:
            return

        self._frame_counter += 1
        frames_per_move = max(1, 60 // self.moves_per_second)
        if self._frame_counter < frames_per_move:
            return
        self._frame_counter = 0

        self.snake.move()

        if self.snake.collides_with_wall(self.grid_width, self.grid_height):
            self.game_over = True
            self._play_sound(self.game_over_sound)
            return

        if self.snake.collides_with_self():
            self.game_over = True
            self._play_sound(self.game_over_sound)
            return

        if self.snake.head_rect().colliderect(self.food.rect()):
            self.snake.grow()
            self.score += 1
            self._play_sound(self.eat_sound)
            self.food.respawn(self.snake.body)

    def render(self, screen):
        # Draw food
        pygame.draw.rect(screen, RED, self.food.rect())

        # Draw snake
        for rect in self.snake.segment_rects():
            pygame.draw.rect(screen, GREEN, rect)

        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        if self.game_over:
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))

            title_text = self.title_font.render("Game Over", True, WHITE)
            score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
            menu_text = self.font.render("1 Easy   2 Medium   3 Hard   4 Exit", True, WHITE)

            screen.blit(title_text, (self.width // 2 - title_text.get_width() // 2, self.height // 2 - 80))
            screen.blit(score_text, (self.width // 2 - score_text.get_width() // 2, self.height // 2 - 20))
            screen.blit(menu_text, (self.width // 2 - menu_text.get_width() // 2, self.height // 2 + 40))
