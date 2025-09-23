import random
from params import *
from sys import exit
from enum import Enum, auto

class Poki(pygame.Rect):
    def __init__(self, img):
        pygame.Rect.__init__(self, poki_x, poki_y, poki_width, poki_height)
        self.img = img


class Column(pygame.Rect):
    def __init__(self, img):
        pygame.Rect.__init__(self, column_x, column_y, column_width, column_height)
        self.img = img
        self.passed = False


class PointsBar(pygame.Rect):
    def __init__(self, img):
        pygame.Rect.__init__(self, 0, 0, 360, 70)
        self.img = img


class GameState(Enum):
    MENU = auto()
    PLAYING = auto()
    GAME_OVER = auto()


class Game:
    def __init__(self):
        self.poki = Poki(poki_image)
        self.columns = []
        self.velocity_x = -2
        self.velocity_y = 0
        self.gravity = 0.4
        self.score = 0
        self.prev_score = -0

        pygame.init()
        pygame.mixer.init()

        self.flap_sound = pygame.mixer.Sound(FLAP_SOUND)
        self.flap_sound.set_volume(0.3)

        self.point_sound = pygame.mixer.Sound(POINT_SOUND)
        self.point_sound.set_volume(0.3)

        self.game_over_sound = pygame.mixer.Sound(GAME_OVER_SOUND)
        self.game_over_sound.set_volume(0.3)

        self.menu_ost = pygame.mixer.Sound(MENU_OST)
        self.menu_ost.set_volume(0.2)
        self.menu_ost.play(loops=-1)

        self.window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
        pygame.display.set_caption("Flappy Kite")
        pygame.display.set_icon(kite_logo)
        self.clock = pygame.time.Clock()

        self.create_columns_timer = pygame.USEREVENT + 0
        pygame.time.set_timer(self.create_columns_timer, 1700)

        self.game_state = GameState.MENU

        self.points_bar = PointsBar(points_bar_image)

        self.button_rect = pygame.Rect(0, 0, 200, 60)
        self.button_rect.center = (GAME_WIDTH // 2, GAME_HEIGHT // 2)

        self.play_again_button = self.create_button(120, 40, 0, 10)
        self.back_to_menu_button = self.create_button(120, 40, 0, 60)

        self.play_button = self.create_button(120, 40, 0, 170)
        self.exit_button = self.create_button(120, 40, 0, 220)

        self.draw()
        pygame.display.update()
        self.clock.tick(60)

        self.record = self.upload_record()

    def upload_record(self):
        try:
            with open(FILE_RECORDS, "r") as f:
                content = f.read().strip()
                return int(content) if content else 0
        except FileNotFoundError:
            return 0
        except ValueError:
            return 0

    def create_button(self, button_width, button_height, button_x, button_y):
        return pygame.Rect(
            (GAME_WIDTH - button_width) // 2 + button_x,
            (GAME_HEIGHT - button_height) // 2 + button_y,
            button_width,
            button_height
        )

    def print_text(self, text, font, font_size, text_x, text_y, color):
        text_font = pygame.font.SysFont(font, font_size)
        text_render = text_font.render(text, True, color)
        text_rect = text_render.get_rect()
        text_rect.center = (text_x, text_y)
        self.window.blit(text_render, text_rect)

    def draw_button(self, text, button, font_size, text_color, button_color, border_rad):
        button_text = pygame.font.SysFont(FONT, font_size).render(text, True, text_color)
        text_rect = button_text.get_rect(center=button.center)
        pygame.draw.rect(self.window, button_color, button, border_radius=border_rad)
        self.window.blit(button_text, text_rect)

    def click_button_effect(self, text, button, font_size, text_color, button_color, border_rad):
        self.draw_button(text, button, font_size, button_color, text_color, border_rad)
        pygame.display.update()
        pygame.time.delay(150)
        self.draw_button(text, button, font_size, text_color, button_color, border_rad)
        pygame.display.update()
        pygame.time.delay(200)

    def draw(self):

        if self.game_state is GameState.PLAYING:
            self.window.blit(background_image, (0, 0))
            self.window.blit(self.poki.img, self.poki)

            for column in self.columns:
                self.window.blit(column.img, column)

            self.window.blit(self.points_bar.img, self.points_bar)
            self.print_text("Score: " + str(int(self.score)), FONT, 30, 80, 30, BROWN)
        elif self.game_state is GameState.GAME_OVER:
            self.window.blit(game_over_image, (0, 0))
            self.print_text("Game Over", FONT, 40, GAME_WIDTH / 2, GAME_HEIGHT / 2 - 260, WHITE)
            score_text, record_text = "Score: ", "Record: "

            prev_record = self.record
            if self.score > self.record:
                score_text = "New record - " + score_text
                record_text = "Previous " + record_text
                with open(FILE_RECORDS, "w") as f:
                    f.write(str(int(self.score)))
                self.record = self.score

            self.print_text(score_text + str(int(self.score)), FONT, 25, GAME_WIDTH / 2, GAME_HEIGHT / 2 - 95, WHITE)
            self.print_text(record_text + str(int(prev_record)), FONT, 20, GAME_WIDTH / 2, GAME_HEIGHT / 2 - 60, WHITE)

            self.draw_button("Play Again", self.play_again_button, 20, BROWN, BEIGE, 10)
            self.draw_button("Menu", self.back_to_menu_button, 20, BROWN, BEIGE, 10)

        else:
            self.window.blit(start_menu_image, (0, 0))
            self.draw_button("Play", self.play_button, 20, BROWN, BEIGE, 10)
            self.draw_button("Exit", self.exit_button, 20, BROWN, BEIGE, 10)

    def control(self):
        self.velocity_y += self.gravity
        self.poki.y += self.velocity_y
        self.poki.y = max(self.poki.y, 0)

        if self.poki.y > GAME_HEIGHT:
            self.game_state = GameState.GAME_OVER
            self.game_over_sound.play()
            pygame.time.delay(TIME_DELAY)
            self.menu_ost.play(loops=-1)
            return

        for column in self.columns:
            column.x += self.velocity_x

            if not column.passed and self.poki.x > column.x + column.width:
                self.score += 0.5
                column.passed = True
                if self.score - self.prev_score == 1:
                    self.point_sound.play()
                    self.prev_score = self.score

            if self.poki.colliderect(column):
                self.game_state = GameState.GAME_OVER
                self.game_over_sound.play()
                pygame.time.delay(TIME_DELAY)
                self.menu_ost.play(loops=-1)
                return

        while len(self.columns) > 0 and self.columns[0].x < -column_width:
            self.columns.pop(0)

    def create_columns(self):
        random_column_y = column_y - column_height / 4 - random.random() * (column_height / 2)
        opening_space = 3 * GAME_HEIGHT / 8

        top_column = Column(top_column_image)
        top_column.y = random_column_y
        self.columns.append(top_column)

        bottom_column = Column(bottom_column_image)
        bottom_column.y = top_column.y + top_column.height + opening_space
        self.columns.append(bottom_column)

    def run(self):

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == self.create_columns_timer and self.game_state is GameState.PLAYING:
                    self.create_columns()

                if event.type == pygame.KEYDOWN and self.game_state is GameState.PLAYING:
                    if event.key in (pygame.K_SPACE, pygame.K_x, pygame.K_UP):
                        self.velocity_y = -6
                        self.flap_sound.play()

                if event.type == pygame.MOUSEBUTTONDOWN and self.game_state is GameState.GAME_OVER:
                    self.poki.y = poki_y
                    self.velocity_y = 0
                    self.columns.clear()
                    self.score = 0
                    self.prev_score = 0
                    if self.play_again_button.collidepoint(event.pos):
                        self.game_state = GameState.PLAYING
                        self.click_button_effect("Play Again", self.play_again_button, 20, BROWN, BEIGE, 10)
                        self.menu_ost.stop()
                    if self.back_to_menu_button.collidepoint(event.pos):
                        self.game_state = GameState.MENU
                        self.click_button_effect("Menu", self.back_to_menu_button, 20, BROWN, BEIGE, 10)
                        self.draw()
                        pygame.display.update()
                        self.clock.tick(60)

                if event.type == pygame.MOUSEBUTTONDOWN and self.game_state is GameState.MENU:
                    if self.play_button.collidepoint(event.pos):
                        self.game_state = GameState.PLAYING
                        self.click_button_effect("Play", self.play_button, 20, BROWN, BEIGE, 10)
                        self.menu_ost.stop()
                    if self.exit_button.collidepoint(event.pos):
                        self.click_button_effect("Exit", self.exit_button, 20, BROWN, BEIGE, 10)
                        pygame.quit()
                        exit()

            if self.game_state is GameState.PLAYING:
                self.control()
                self.draw()
                pygame.display.update()
                self.clock.tick(60)