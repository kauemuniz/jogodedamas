import pygame
from .constantes import BLACK, ROWS, RED, TAMANHO_QUADRADO, COLS, WHITE
from .pecas import Piece


class Board:

    """
    Representa o tabuleiro do jogo de damas, gerenciando as peças e suas posições.

    Atributos:
        board (list): Uma matriz de listas que representa as posições das peças no tabuleiro.
        red_left (int): Contagem de peças vermelhas restantes no jogo.
        white_left (int): Contagem de peças brancas restantes no jogo.
        red_kings (int): Contagem de peças vermelhas que foram promovidas a reis.
        white_kings (int): Contagem de peças brancas que foram promovidas a reis.

    Relacionamentos:
        - Composição com a classe Piece: Board cria e gerencia objetos Piece.
    """
    def __init__(self):
        self.board = []
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0
        self.create_board()

    def draw_squares(self, win):

        """
        Desenha os quadrados do tabuleiro alternando as cores.

        Parâmetros:
            win (pygame.Surface): A superfície onde o tabuleiro será desenhado.
        """
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, WHITE, (row * TAMANHO_QUADRADO, col * TAMANHO_QUADRADO, TAMANHO_QUADRADO, TAMANHO_QUADRADO))

    def move(self, piece, row, col):

        """
        Move uma peça para uma nova posição no tabuleiro.

        Parâmetros:
            piece (Piece): A peça a ser movida.
            row (int): A linha destino da peça.
            col (int): A coluna destino da peça.
        """
        # Atualiza as posições no array do tabuleiro e verifica se a peça deve se tornar um rei.

        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.red_kings += 1

    def get_piece(self, row, col):
        """
        Retorna a peça na posição especificada.

        Parâmetros:
            row (int): A linha da peça.
            col (int): A coluna da peça.
        
        Retorna:
            Piece: A peça na posição especificada, ou None se não houver peça.
        """
        return self.board[row][col]

    def create_board(self):

        """
        Inicializa o tabuleiro colocando as peças nas posições de início padrão para um jogo de damas.
        """
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, win):
        """
        Desenha o tabuleiro e todas as peças.

        Parâmetros:
            win (pygame.Surface): A superfície onde o tabuleiro será desenhado.
        """
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):
        """
        Remove uma ou mais peças do tabuleiro.

        Parâmetros:
            pieces (list): Lista de peças a serem removidas.
        """
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED:
                    self.red_left -= 1
                else:
                    self.white_left -= 1

    def winner(self):
        """
        Determina se há um vencedor com base no número de peças restantes.

        Retorna:
            str: Retorna 'RED' ou 'WHITE' indicando o vencedor, ou None se ainda não houver vencedor.
        """
        if self.red_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return RED

        return None

    def get_valid_moves(self, piece):
        """
        Calcula todos os movimentos válidos para uma peça dada.

        Parâmetros:
            piece (Piece): A peça para a qual os movimentos serão calculados.
        
        Retorna:
            dict: Um dicionário com as posições de destino como chaves e as peças a serem capturadas como valores.
        """
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == RED or piece.king:
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))

        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):

        """
        Auxilia no cálculo de movimentos válidos para a esquerda.

        Parâmetros:
            start (int): Linha inicial para verificação.
            stop (int): Linha final para verificação.
            step (int): Passo de incremento ou decremento para o loop.
            color (tuple): Cor da peça que está sendo movida.
            left (int): Coluna inicial para verificação.
            skipped (list): Peças que foram puladas em movimentos anteriores.
        
        Retorna:
            dict: Movimentos válidos encontrados nesta direção.
        """
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row, step, color, left - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, left + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1

        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):

        """
        Auxilia no cálculo de movimentos válidos para a direita.

        Parâmetros:
            start (int): Linha inicial para verificação.
            stop (int): Linha final para verificação.
            step (int): Passo de incremento ou decremento para o loop.
            color (tuple): Cor da peça que está sendo movida.
            right (int): Coluna inicial para verificação.
            skipped (list): Peças que foram puladas em movimentos anteriores.
        
        Retorna:
            dict: Movimentos válidos encontrados nesta direção.
        """
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break

            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row, step, color, right - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, right + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1

        return moves