import pygame
from damas.constantes import WIDTH, HEIGHT, TAMANHO_QUADRADO, RED
from damas.jogo import Game


FPS = 70

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Damas')


def get_row_col_from_mouse(pos):

    """
    Converte a posição do mouse em coordenadas de linha e coluna no tabuleiro.

    Parâmetros:
        pos (tuple): Posição (x, y) do mouse na tela.

    Retorna:
        tuple: Correspondente (linha, coluna) no tabuleiro de damas.
    """
    x, y = pos
    row = y // TAMANHO_QUADRADO
    col = x // TAMANHO_QUADRADO
    return row, col


def main():

    """
    Função principal que executa o jogo. Inicializa o jogo e entra no loop principal.
    """
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:
        # Mantém o jogo rodando na taxa de quadros especificada
        clock.tick(FPS)

        # Verifica se há um vencedor e encerra o loop se houver
        if game.winner() != None:
            print(game.winner())
            run = False
        # Event Loop: Gerencia eventos como fechar a janela e cliques do mouse
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)
        
        # Atualiza o estado do jogo e redesenha a janela
        game.update()

    # Fecha a janela do Pygame e encerra o programa
    pygame.quit()


main()