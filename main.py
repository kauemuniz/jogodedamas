import pygame
from damas.constantes import WIDTH, HEIGHT, TAMANHO_QUADRADO, RED
from damas.jogo import Game


FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Damas')


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // TAMANHO_QUADRADO
    col = x // TAMANHO_QUADRADO
    return row, col


def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:
        clock.tick(FPS)

        if game.winner() != None:
            print(game.winner())
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()

    pygame.quit()


main()