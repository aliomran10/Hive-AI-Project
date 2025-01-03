import pygame as pg
from settings import WHITE, BLACK, PANEL, WIDTH


class Turn_Panel:

    def __init__(self):
        outline_width = WIDTH / 4
        outline_height = 40

        self.inner_left = 5
        self.inner_top = 5
        self.inner_width = outline_width - 10
        self.inner_height = outline_height - 10

        self.back_panel = pg.Rect(0, 0, outline_width, outline_height)
        self.inner_panel = pg.Rect(self.inner_left, self.inner_top, self.inner_width, self.inner_height)

    def draw(self, background, turn):
        FONT = pg.font.SysFont('Times New Norman', 32)
        if turn % 2 == 1:  # turn starts at 1
            font = FONT.render('Player 1 Turn:', True, WHITE)
        else:
            font = FONT.render('Player 2 Turn:', True, WHITE)
        title_rect = font.get_rect(center=(self.inner_left + self.inner_width * (2 / 5), self.inner_top + self.inner_height / 2))

        pg.draw.rect(background, BLACK, self.back_panel)
        pg.draw.rect(background, PANEL, self.inner_panel)

        if turn % 2 == 1:
            pg.draw.circle(background, WHITE, (self.inner_left + self.inner_width * (7 / 8), self.inner_top + self.inner_height / 2), 13)
        else:
            pg.draw.circle(background, BLACK, (self.inner_left + self.inner_width * (7 / 8), self.inner_top + self.inner_height / 2), 13)

        background.blit(font, title_rect)
        pg.display.flip()

    def copy(self):
        # Create a new instance
        new_panel = Turn_Panel()

        # Copy attributes
        new_panel.inner_left = self.inner_left
        new_panel.inner_top = self.inner_top
        new_panel.inner_width = self.inner_width
        new_panel.inner_height = self.inner_height
        new_panel.back_panel = self.back_panel.copy()
        new_panel.inner_panel = self.inner_panel.copy()

        return new_panel