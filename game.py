import sys
import pygame
import square
import utils
import pieces
import board
from game_types import GameInterface

SAMPLE = """
		Black
  A B C D E F G H -- Files
1 W B W B W B W B
2 B W B W B W B W
3 W B W B W B W B
4 B W B W B W B W
5 W B W B W B W B
6 B W B W B W B W
7 W B W B W B W B
8 B W B W B W B W
		White
"""


class Game(GameInterface):
    """Game holds logic of chess game"""

    def __init__(self):
        self.__board: dict[str, pieces.Piece] = {}
        self.__screen = None

        self.last_file = utils.File_A
        self.last_rank = utils.Rank_1
        self.__available_moves: set[str] = {}

        # indicate which side can move
        self.__turn = utils.Color.BLACK

    def set_screen(self, screen: board.GameRenderer):
        """set display screen for the game"""
        self.__screen = screen

    def switch_turn(self) -> None:
        """Toggle turns for players"""
        if self.__turn == utils.Color.WHITE:
            self.__turn = utils.Color.BLACK
            return
        self.__turn = utils.Color.WHITE

    def __init_board(self) -> None:
        for rank in utils.RANKS:
            for file in utils.FILES:
                square_name = utils.create_square_name(file, rank)
                self.__board[square_name] = None

    def re_organize_board(self) -> None:
        """Place pieces in their initial places for a new game"""
        piece_classes = [
            pieces.PieceRook,
            pieces.PieceKnight,
            pieces.PieceBishop,
            pieces.PieceQueen,
            pieces.PieceKing,
            pieces.PieceBishop,
            pieces.PieceKnight,
            pieces.PieceRook,
        ]
        for index, file in enumerate(utils.FILES):
            for item in [
                (utils.Color.BLACK, utils.Rank_2),
                (utils.Color.WHITE, utils.Rank_7),
            ]:
                piece = pieces.PiecePawn(color=item[0])
                square_name = utils.create_square_name(file, item[1])

                self.__board[square_name] = piece
                self.__screen.draw_on_square(square_name, piece=piece)

            piece_class = piece_classes[index]
            for item in [
                (utils.Color.BLACK, utils.Rank_1),
                (utils.Color.WHITE, utils.Rank_8),
            ]:
                piece = piece_class(color=item[0])
                square_name = utils.create_square_name(file, item[1])

                self.__board[square_name] = piece
                self.__screen.draw_on_square(square_name, piece=piece)

    def get_board(self) -> dict[str, square.Square]:
        """getter for accessing game board state"""
        return self.__board

    def reset_game(self) -> None:
        """Re initialize board and re orginaze pieces"""
        self.__init_board()
        self.re_organize_board()

    def check_2_cells_hold_enemies(
        self, square_name_1: str, square_name_2: str
    ) -> bool:
        """Checks if 2 cells are within board and hold 2 pieces with different color"""
        if square_name_1 not in self.__board or square_name_2 not in self.__board:
            return False

        piece_1 = self.__board[square_name_1]
        if not piece_1:
            return False

        piece_2 = self.__board[square_name_2]
        if not piece_2:
            return False

        return piece_2.color != piece_1.color

    def check_square_occupied(self, square_name: str) -> bool:
        """
        Check if given square is holding any piece.
        If yes, returns `True`, `False` otherwise.
        If `square_name` is outside of board, return `True`
        """
        if not square_name in self.__board:
            return True
        return self.__board[square_name] is not None

    def handle_mouse_down(self, event: pygame.event.Event):
        """listener for left mouse click up event"""
        (position_x, position_y) = event.dict["pos"]
        file = position_x // utils.SQUARE_SIZE + utils.File_A
        rank = position_y // utils.SQUARE_SIZE + utils.Rank_1

        square_name = utils.create_square_name(file, rank)
        piece = self.__board.get(square_name)
        if not piece and square_name in self.__available_moves:
            self.__screen.draw_on_square(square_name, piece=piece)
            self.__screen.draw_on_square()
            self.__available_moves.clear()
        else:
            self.__available_moves = piece.calculate_next_moves((file, rank), self)
            for move in self.__available_moves:
                self.__screen.draw_on_square(move, True)

    def event_handler(self, event: pygame.event.Event):
        """event listener for game events"""
        if event.type == pygame.QUIT:
            self.__close()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.handle_mouse_down(event)

    def run(self):
        """run the game"""
        self.__screen.setup()  # this must go first
        self.__init_board()
        self.re_organize_board()
        self.__screen.render()

    def __close(self):
        self.__board.clear()
        self.__screen.close()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game_ui = board.GameRenderer(game.event_handler)
    game.set_screen(game_ui)
    game.run()
