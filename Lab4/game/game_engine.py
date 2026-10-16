
import pygame
from .bird import Bird
from .pipe import Pipe

WHITE = (255, 255, 255)
GREEN = (0, 150, 0)
BLACK = (0, 0, 0)
GRAY = (190, 190, 190)
YELLOW = (255, 220, 0)


class GameEngine:
    DIFFICULTIES = {
        "Easy": {"speed": 3, "gap": 190, "interval": 100},
        "Medium": {"speed": 4, "gap": 150, "interval": 90},
        "Hard": {"speed": 6, "gap": 120, "interval": 80},
    }

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.font = pygame.font.SysFont("Arial", 30)
        self.title_font = pygame.font.SysFont("Arial", 48, bold=True)
        self.option_font = pygame.font.SysFont("Arial", 27)

        self.difficulty = "Medium"
        self.game_over = False
        self.started = False
        self._game_over_logged = False

        self.reset_game()

    def reset_game(self):
        """Reset gameplay while keeping the selected difficulty."""
        settings = self.DIFFICULTIES[self.difficulty]

        self.bird = Bird(self.width // 4, self.height // 2)

        self.pipe_speed = settings["speed"]
        self.pipe_gap = settings["gap"]
        self.pipe_interval = settings["interval"]

        self._spawn_timer = 0
        self.pipes = [
            Pipe(
                self.width + 100,
                self.height,
                gap=self.pipe_gap,
                speed=self.pipe_speed,
            )
        ]

        self.score = 0
        self.game_over = False
        self.started = False
        self._game_over_logged = False

    def select_difficulty(self, difficulty):
        if difficulty in self.DIFFICULTIES:
            self.difficulty = difficulty
            self.reset_game()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit

            if self.game_over:
                if event.key == pygame.K_r:
                    # Replay using the current difficulty.
                    self.reset_game()
                    return

                if event.key == pygame.K_1:
                    self.select_difficulty("Easy")
                    return

                if event.key == pygame.K_2:
                    self.select_difficulty("Medium")
                    return

                if event.key == pygame.K_3:
                    self.select_difficulty("Hard")
                    return

                if event.key == pygame.K_q:
                    pygame.quit()
                    raise SystemExit

            if event.key == pygame.K_SPACE and not self.game_over:
                self.started = True
                self.bird.flap()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.game_over:
                # Click the options shown on the Game Over screen.
                mouse_x, mouse_y = event.pos
                center_x = self.width // 2

                if self.height // 2 + 70 <= mouse_y <= self.height // 2 + 110:
                    if center_x - 170 <= mouse_x <= center_x - 65:
                        self.select_difficulty("Easy")
                        return

                    if center_x - 55 <= mouse_x <= center_x + 55:
                        self.select_difficulty("Medium")
                        return

                    if center_x + 65 <= mouse_x <= center_x + 170:
                        self.select_difficulty("Hard")
                        return

                if self.height // 2 + 125 <= mouse_y <= self.height // 2 + 175:
                    if center_x - 120 <= mouse_x <= center_x + 120:
                        self.reset_game()
                        return

                if self.height // 2 + 180 <= mouse_y <= self.height // 2 + 225:
                    if center_x - 120 <= mouse_x <= center_x + 120:
                        pygame.quit()
                        raise SystemExit
            else:
                self.started = True
                self.bird.flap()

    def handle_input(self):
        pass

    def update(self):
        if self.game_over or not self.started:
            return

        self.bird.update()

        if (
            self.bird.y - self.bird.radius <= 0
            or self.bird.y + self.bird.radius >= self.height
        ):
            self.game_over = True
            return

        self._spawn_timer += 1

        if self._spawn_timer >= self.pipe_interval:
            self._spawn_timer = 0
            self.pipes.append(
                Pipe(
                    self.width,
                    self.height,
                    gap=self.pipe_gap,
                    speed=self.pipe_speed,
                )
            )

        for pipe in self.pipes:
            old_top = pipe.top_rect().copy()
            old_bottom = pipe.bottom_rect().copy()

            pipe.move()

            top = pipe.top_rect()
            bottom = pipe.bottom_rect()
            bird_rect = self.bird.rect()

            # Existing full-rectangle collision detection.
            if bird_rect.colliderect(top) or bird_rect.colliderect(bottom):
                self.game_over = True
            else:
                # Existing swept collision check.
                swept_left = min(old_top.left, top.left)
                swept_right = max(old_top.right, top.right)
                swept_width = swept_right - swept_left

                swept_top = pygame.Rect(
                    swept_left, top.top, swept_width, top.height
                )
                swept_bottom = pygame.Rect(
                    swept_left, bottom.top, swept_width, bottom.height
                )

                if (
                    bird_rect.colliderect(swept_top)
                    or bird_rect.colliderect(swept_bottom)
                ):
                    self.game_over = True

            if not pipe.scored and pipe.x + pipe.width < self.bird.x:
                pipe.scored = True
                self.score += 1

        self.pipes = [p for p in self.pipes if not p.off_screen()]

    def draw_text(self, screen, text, font, color, center):
        surface = font.render(text, True, color)
        rect = surface.get_rect(center=center)
        screen.blit(surface, rect)

    def render(self, screen):
        # Preserve the existing game rendering.
        for pipe in self.pipes:
            pygame.draw.rect(screen, GREEN, pipe.top_rect())
            pygame.draw.rect(screen, GREEN, pipe.bottom_rect())

        pygame.draw.circle(
            screen,
            WHITE,
            (int(self.bird.x), int(self.bird.y)),
            self.bird.radius,
        )

        score_text = self.font.render(
            f"Score: {self.score}", True, WHITE
        )
        screen.blit(score_text, (10, 10))

        if not self.started and not self.game_over:
            self.draw_text(
                screen,
                f"Difficulty: {self.difficulty}",
                self.font,
                YELLOW,
                (self.width // 2, 50),
            )
            self.draw_text(
                screen,
                "Press SPACE or click to start",
                self.option_font,
                WHITE,
                (self.width // 2, 90),
            )

        if self.game_over:
            overlay = pygame.Surface(
                (self.width, self.height), pygame.SRCALPHA
            )
            overlay.fill((0, 0, 0, 190))
            screen.blit(overlay, (0, 0))

            center_x = self.width // 2
            center_y = self.height // 2

            self.draw_text(
                screen, "GAME OVER", self.title_font,
                WHITE, (center_x, center_y - 105)
            )
            self.draw_text(
                screen, f"Final Score: {self.score}", self.font,
                WHITE, (center_x, center_y - 55)
            )
            self.draw_text(
                screen, f"Difficulty: {self.difficulty}", self.font,
                YELLOW, (center_x, center_y - 15)
            )

            # Difficulty selection options.
            self.draw_text(
                screen, "[1] EASY", self.option_font,
                YELLOW if self.difficulty == "Easy" else WHITE,
                (center_x - 115, center_y + 90)
            )
            self.draw_text(
                screen, "[2] MEDIUM", self.option_font,
                YELLOW if self.difficulty == "Medium" else WHITE,
                (center_x, center_y + 90)
            )
            self.draw_text(
                screen, "[3] HARD", self.option_font,
                YELLOW if self.difficulty == "Hard" else WHITE,
                (center_x + 115, center_y + 90)
            )

            self.draw_text(
                screen, "[R] Replay", self.option_font,
                WHITE, (center_x, center_y + 145)
            )
            self.draw_text(
                screen, "[Q] Exit", self.option_font,
                WHITE, (center_x, center_y + 195)
            )
            self.draw_text(
                screen, "Or click an option above",
                pygame.font.SysFont("Arial", 19),
                GRAY, (center_x, center_y + 225)
            )

            if not self._game_over_logged:
                print("Game over! Final score:", self.score)
                self._game_over_logged = True
