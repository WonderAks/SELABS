
import pygame
import random


class Pipe:
    def __init__(self, x, screen_height, gap=150, width=70, speed=4):
        self.x = x
        self.width = width
        self.gap = gap
        self.speed = speed
        self.screen_height = screen_height

        # Keep the gap within valid screen boundaries.
        min_gap_y = 50
        max_gap_y = max(
            min_gap_y,
            screen_height - gap - 50
        )
        self.gap_y = random.randint(min_gap_y, max_gap_y)

        self.scored = False

    def move(self):
        self.x -= self.speed

    def off_screen(self):
        return self.x + self.width < 0

    def top_rect(self):
        return pygame.Rect(
            int(self.x), 0, self.width, self.gap_y
        )

    def bottom_rect(self):
        bottom_y = self.gap_y + self.gap
        return pygame.Rect(
            int(self.x),
            bottom_y,
            self.width,
            self.screen_height - bottom_y
        )
