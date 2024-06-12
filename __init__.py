import game
import board


if __name__ == "__main__":
    game = game.Game()
    game_ui = board.GameRenderer(game.event_handler)
    game.set_screen(game_ui)
    game.run()
