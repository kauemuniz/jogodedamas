from .constantes import RED, WHITE, TAMANHO_QUADRADO, GREY, CROWN
import pygame


class Piece:
    PADDING = 15
    OUTLINE = 2

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        self.x = TAMANHO_QUADRADO * self.col + TAMANHO_QUADRADO // 2
        self.y = TAMANHO_QUADRADO * self.row + TAMANHO_QUADRADO // 2

    def make_king(self):
        self.king = True

    def draw(self, win):
        radius = TAMANHO_QUADRADO // 2 - self.PADDING
        pygame.draw.circle(win, GREY, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        if self.king:
            win.blit(CROWN, (self.x - CROWN.get_width() // 2, self.y - CROWN.get_height() // 2))

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

    def __repr__(self):
        return str(self.color)