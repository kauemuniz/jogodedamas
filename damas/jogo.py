import pygame
from .constantes import RED, WHITE, BLUE, TAMANHO_QUADRADO
from damas.tabuleiro import Board


class Game:

    """
    Classe principal do jogo que gerencia o estado do jogo, incluindo o tabuleiro,
    turno dos jogadores, e movimentos válidos.

    Atributos:
        win (pygame.Surface): A janela onde o jogo é desenhado.
        selected (Piece): A peça atualmente selecionada pelo jogador.
        board (Board): O tabuleiro do jogo, gerenciando todas as peças.
        turn (tuple): A cor do jogador atual, controlando de quem é a vez.
        valid_moves (dict): Dicionário de movimentos válidos para a peça selecionada.
    
    Relacionamentos:
        - Usa objetos da classe Board para gerenciar o estado do tabuleiro.
        - Interage indiretamente com objetos da classe Piece através de métodos em Board.
    """
    def __init__(self, win):

        """
        Inicializa o jogo configurando o tabuleiro e a interface de usuário.

        Parâmetros:
            win (pygame.Surface): A superfície onde o jogo será desenhado.
        """
        self._init()
        self.win = win

    def update(self):

        """
        Atualiza o display do jogo, redesenhando o tabuleiro e os movimentos válidos.
        """
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self):

        """
        Reinicializa o jogo para seu estado inicial, preparando o tabuleiro e
        definindo o jogador inicial como RED.
        """
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}

    def winner(self):

        """
        Delega a verificação de vencedor para o método winner do tabuleiro.
        Retorna:
            str: A cor do vencedor, se houver algum.
        """
        return self.board.winner()

    def reset(self):

        """
        Reinicia o jogo para o estado inicial.
        """
        self._init()

    def select(self, row, col):

        """
        Seleciona uma peça ou tenta mover uma peça selecionada para uma nova posição.

        Parâmetros:
            row (int): A linha da peça a ser selecionada ou destino do movimento.
            col (int): A coluna da peça a ser selecionada ou destino do movimento.
        
        Retorna:
            bool: True se uma peça foi selecionada ou um movimento foi realizado com sucesso.
        """

        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)

        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True

        return False

    def _move(self, row, col):

        """
        Realiza um movimento de uma peça selecionada para uma nova posição, se válido.

        Parâmetros:
            row (int): A linha destino do movimento.
            col (int): A coluna destino do movimento.
        
        Retorna:
            bool: True se o movimento foi realizado com sucesso, False caso contrário.
        """

        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False

        return True

    def draw_valid_moves(self, moves):

        """
        Desenha círculos no tabuleiro para indicar movimentos válidos para a peça selecionada.

        Parâmetros:
            moves (dict): Um dicionário de movimentos válidos com posições como chaves.
        """
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE,
                               (col * TAMANHO_QUADRADO + TAMANHO_QUADRADO // 2, row * TAMANHO_QUADRADO + TAMANHO_QUADRADO // 2), 15)

    def change_turn(self):

        """
        Alterna a vez entre os dois
        """
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED