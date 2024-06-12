import sys
import utils
import pieces
import board
from game_types import GameInterface
from typing import Optional, Any

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
        self.__board: dict[str, Optional[pieces.Piece]] = {}
        self.__screen = None
        self.last_file = utils.File_A
        self.last_rank = utils.Rank_1
        self.__available_moves: set[str] = set()
        self.__turn_color = utils.Color.BLACK
        self.__active_square: Optional[str] = None
        self.__captures_data = {
            utils.Color.BLACK: [],
            utils.Color.WHITE: [],
        }

    def set_screen(self, screen: board.GameRenderer):
        """set display screen for the game"""
        self.__screen = screen

    def switch_turn(self) -> None:
        """Toggle turns for players"""
        self.__turn_color = (
            utils.Color.BLACK if self.__turn_color == utils.Color.WHITE else utils.Color.WHITE
        )

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
                self.__screen.draw_piece_on_square(
                    square_name, piece_name=piece.__str__()
                )

            piece_class = piece_classes[index]
            for item in [
                (utils.Color.BLACK, utils.Rank_1),
                (utils.Color.WHITE, utils.Rank_8),
            ]:
                piece = piece_class(color=item[0])
                square_name = utils.create_square_name(file, item[1])

                self.__board[square_name] = piece
                self.__screen.draw_piece_on_square(
                    square_name, piece_name=piece.__str__()
                )

    def get_board(self) -> dict[str, Optional[Any]]:
        """getter for accessing game board state"""
        return self.__board

    def reset_game(self) -> None:
        """Re initialize board and re orginaze pieces"""
        self.__init_board()
        self.re_organize_board()

    def check_2_squares_hold_enemies(
        self, square_name_1: str, square_name_2: str
    ) -> bool:
        """Checks if 2 cells are within board and hold 2 pieces with different color"""
        piece_1 = self.__board.get(square_name_1)
        piece_2 = self.__board.get(square_name_2)

        return piece_1 and piece_2 and piece_2.color != piece_1.color

    def check_square_occupied(self, square_name: str) -> bool:
        """
        Check if given square is holding any piece.
        If yes, returns `True`, `False` otherwise.
        If `square_name` is outside of board, return `True`
        """
        return square_name not in self.__board or self.__board[square_name] is not None

    def move_piece_from_source_to_dest(self, source_sq: str, dest_sq: str) -> None:
        if source_sq not in self.__board or dest_sq not in self.__board:
            return

        self.__screen.draw_piece_on_square(dest_sq, self.__board[source_sq].__str__())
        original_color = utils.SQUARES_COLOR_MAP[source_sq]
        self.__screen.set_color_on_square(source_sq, original_color)
        self.__board[dest_sq] = self.__board[source_sq]
        self.__board[source_sq] = None

    def handle_cell_select(self, event: utils.GameEvent):
        """listener for left mouse click event"""

        file_rank = event.to_file_rank()
        selected_square_name = utils.create_square_name(*file_rank)

        if self.__active_square and len(self.__available_moves) > 0:
            # means user is moving pieces
            if selected_square_name in self.__available_moves:
                for sq_name in self.__available_moves | {self.__active_square}:
                    original_color = utils.SQUARES_COLOR_MAP[sq_name]
                    self.__screen.set_color_on_square(sq_name, original_color)

                self.move_piece_from_source_to_dest(
                    self.__active_square, selected_square_name
                )
                self.__active_square = None
                self.__available_moves = set()
                self.switch_turn()

            else:
                for cell_name in self.__available_moves:
                    original_color = utils.SQUARES_COLOR_MAP[cell_name]
                    self.__screen.set_color_on_square(cell_name, original_color)
                self.__active_square = None
                self.__available_moves = set()

        elif self.check_selected_square_holds_piece_in_turn(selected_square_name):
            # means user is choosing piece to move
            piece = self.__board[selected_square_name]
            self.__available_moves = piece.calculate_next_moves(file_rank, self)
            self.__active_square = selected_square_name

            for square_name in self.__available_moves:
                self.__screen.set_color_on_square(square_name, utils.Color.GREEN)

    def event_handler(self, event: utils.GameEvent):
        """event listener for game events"""
        if event.event_type == utils.GameEventType.QUIT:
            self.__close()
        elif event.event_type == utils.GameEventType.MOUSE_CLICK:
            self.handle_cell_select(event)

    def check_selected_square_holds_piece_in_turn(self, square_name: str) -> bool:
        """check if selected cell contains a piece with color match turn color"""
        piece = self.__board.get(square_name)
        return piece and piece.color == self.__turn_color

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
