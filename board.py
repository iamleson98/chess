# from enum import Enum
# import sys
from typing import Tuple, Dict, Callable, Any
import utils
import pygame
import pieces


class GameRenderer:
    def __init__(self, event_listener: Callable[[Any, pygame.event.Event], None]):
        pygame.init()
        self.__images: Dict[str, pygame.Surface] = {}
        self.__squares: Dict[str, Tuple[int, int]] = {}
        self.__screen = pygame.display.set_mode(
            (utils.SCREEN_DIMENSION, utils.SCREEN_DIMENSION)
        )
        self.__event_listener = event_listener
        self.__clock = pygame.time.Clock()

    def setup(self):
        """load game resources, draw board"""
        self.__load_images()
        self.__classify_board()

    def close(self):
        """free up resource"""
        self.__images.clear()
        self.__squares.clear()
        pygame.quit()

    def __load_images(self):
        try:
            board_image = pygame.image.load(utils.GAME_BOARD)
            self.__screen.blit(
                board_image, (0, 0)
            )  # draw board image before other pieces
            pygame.display.flip()
        except Exception as e:
            print(f"load image {utils.GAME_BOARD} error: {e}")
            self.close()

        for path in utils.PiecePath:
            try:
                image = pygame.image.load(path.value)
                image_width = image.get_width()
                image_height = image.get_height()
                scale_factor_x = utils.SQUARE_SIZE / image_width
                scale_factor_y = utils.SQUARE_SIZE / image_height
                scale_factor = min(scale_factor_x, scale_factor_y)

                image = pygame.transform.scale(
                    image,
                    (int(image_width * scale_factor), int(image_height * scale_factor)),
                )
                self.__images[path.name] = image
            except Exception as e:
                print(f"load image {path.name} error: {e}")
                self.close()

    def __classify_board(self):
        for rank_index, rank in enumerate(utils.RANKS):
            for file_index, file_ in enumerate(utils.FILES):
                square_name = utils.create_square_name(file_, rank)

                self.__squares[square_name] = (
                    file_index * utils.SQUARE_SIZE,
                    rank_index * utils.SQUARE_SIZE,
                )

    def draw_on_square(
        self, square_name: str, mark_green: bool = False, piece: pieces.Piece = None
    ):
        """
        If `piece` is `None`, then reset color for square
        """
        coordination = self.__squares.get(square_name)
        if not coordination:
            print(f"draw_on_square. {square_name} is invalid")
            return

        if piece:
            image_name = utils.calculate_image_key(piece.piece_type, piece.color)
            image = self.__images[image_name]
            self.__screen.blit(image, coordination)
        else:
            color = (
                utils.Color.GREEN.value
                if mark_green
                else utils.SQUARES_COLOR_MAP.get(square_name)
            )
            pygame.draw.rect(
                self.__screen,
                color,
                (
                    coordination[0],
                    coordination[1],
                    utils.SQUARE_SIZE,
                    utils.SQUARE_SIZE,
                ),
            )

        pygame.display.flip()

    def render(self):
        """render game interface"""
        while True:
            for event in pygame.event.get():
                self.__event_listener(event)
            self.__clock.tick(5)
            # pygame.display.flip()
            # pygame.event.pump()
