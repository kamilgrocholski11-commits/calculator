import pygame

from settings import SCREEN_WIDTH, SCREEN_HEIGHT, START_MONEY
from menu import Menu
from game import Game


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Workers Defense")

    menu = Menu(screen)
    state = "menu"

    while True:
        if state == "menu":
            result = menu.run()
            if result == "quit":
                break
            state = "game"
            game = Game(
                screen,
                result["map"],
                result["difficulty"],
                result.get("equipped_units", ["Worker"]),
                result.get("money", START_MONEY),
            )
        elif state == "game":
            state = game.run()
            if state == "quit":
                break
            if state == "menu":
                continue
        else:
            break

    pygame.quit()


if __name__ == "__main__":
    main()
