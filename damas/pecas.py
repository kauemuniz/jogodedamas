from .constantes import RED, WHITE, TAMANHO_QUADRADO, GREY, CROWN
import pygame


class Piece:

    """
    Representa uma única peça no jogo de damas.

    Atributos:
        row (int): Linha atual da peça no tabuleiro.
        col (int): Coluna atual da peça no tabuleiro.
        color (tuple): Cor da peça, que também indica a equipe da peça (RED ou WHITE).
        king (bool): Indica se a peça foi promovida a rei.
        x (int): Posição x do centro da peça na janela do jogo.
        y (int): Posição y do centro da peça na janela do jogo.

    Métodos:
        calc_pos(): Calcula as posições x e y com base na posição da linha e da coluna.
        make_king(): Promove a peça a rei.
        draw(win): Desenha a peça na janela do jogo.
        move(row, col): Atualiza a posição da peça após um movimento.
        __repr__(): Representação em string da peça, principalmente para debugging.
    """


    PADDING = 15
    OUTLINE = 2

    def __init__(self, row, col, color):

        """
        Inicializa uma peça com a cor, posição e status de rei especificados.

        Parâmetros:
            row (int): A linha onde a peça será posicionada.
            col (int): A coluna onde a peça será posicionada.
            color (tuple): A cor da peça (RED ou WHITE).
        """
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):

        """
        Calcula a posição central da peça na tela com base em sua linha e coluna no tabuleiro.
        """
        self.x = TAMANHO_QUADRADO * self.col + TAMANHO_QUADRADO // 2
        self.y = TAMANHO_QUADRADO * self.row + TAMANHO_QUADRADO // 2

    def make_king(self):

        """
        Promove a peça a rei, alterando seu status e permitindo que se mova para trás.
        """ 
        self.king = True

    def draw(self, win):

        """
        Desenha a peça na janela especificada com detalhes visuais que indicam se é um rei.

        Parâmetros:
            win (pygame.Surface): A superfície onde a peça será desenhada.
        """
         
        radius = TAMANHO_QUADRADO // 2 - self.PADDING
        pygame.draw.circle(win, GREY, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        if self.king:
            win.blit(CROWN, (self.x - CROWN.get_width() // 2, self.y - CROWN.get_height() // 2))

    def move(self, row, col):

        """
        Atualiza a posição da peça após um movimento.

        Parâmetros:
            row (int): Nova linha para a peça.
            col (int): Nova coluna para a peça.
        """
        self.row = row
        self.col = col
        self.calc_pos()

    def __repr__(self):

        """
        Fornece uma representação em string da peça, útil para debugging.

        Retorna:
            str: Representação da cor da peça.
        """
        return str(self.color)