from abc import ABC, abstractmethod
import uuid
from dataclasses import dataclass
import utils
from game_types import GameInterface


@dataclass
class Piece(ABC):
    """base class for other pieces"""

    color: utils.Color
    piece_type: utils.PieceType
    id: str = str(uuid.uuid4())

    @abstractmethod
    def calculate_available_moves(
        self, current_position: tuple[int, int], game: GameInterface
    ) -> set[str]:
        """`current_position[0]` is `file`, `current_position[1]` is `rank`"""

    def __str__(self) -> str:
        return f"{self.color.name}_{self.piece_type.name}"


@dataclass
class PiecePawn(Piece):
    """pawn piece"""

    piece_type: utils.PieceType = utils.PieceType.PAWN

    def calculate_available_moves(
        self, current_position: tuple[int, int], game: GameInterface
    ) -> set[str]:
        moves: set[str] = set()

        rank_delta = 1 if self.color == utils.Color.BLACK else -1

        front_square_name = utils.create_square_name(
            current_position[0], current_position[1] + rank_delta
        )
        if not game.check_square_occupied(front_square_name):
            moves.add(front_square_name)

            if self.is_initial_position(current_position):
                rank_delta = 2
                if self.color == utils.Color.WHITE:
                    rank_delta = -2

                front_square_name = utils.create_square_name(
                    current_position[0], current_position[1] + rank_delta
                )
                if not game.check_square_occupied(front_square_name):
                    moves.add(front_square_name)

        capture_detals = (
            [[-1, 1], [1, 1]]
            if self.color == utils.Color.BLACK
            else [[-1, -1], [1, -1]]
        )

        current_position_name = utils.create_square_name(*current_position)
        for file_delta, rank_delta in capture_detals:
            capture_position_name = utils.create_square_name(
                current_position[0] + file_delta, current_position[1] + rank_delta
            )
            if game.check_2_squares_hold_enemies(
                current_position_name, capture_position_name
            ):
                moves.add(capture_position_name)

        return moves

    def is_initial_position(self, current_position: tuple[int, int]) -> bool:
        """check if current pawn is standing at its initial position"""
        if self.color == utils.Color.BLACK:
            return current_position[1] == utils.Rank_2
        return current_position[1] == utils.Rank_7


KNIGHT_MOVE_DELTAS = [
    [2, 1],
    [1, 2],
    [-1, 2],
    [-2, 1],
    [2, -1],
    [1, -2],
    [-1, -2],
    [-2, -1],
]


@dataclass
class PieceKnight(Piece):
    """knight piece"""

    piece_type: utils.PieceType = utils.PieceType.KNIGHT

    def calculate_available_moves(
        self, current_position: tuple[int, int], game: GameInterface
    ) -> set[str]:
        current_position_name = utils.create_square_name(*current_position)
        moves: set[str] = set()

        for file_delta, rank_delta in KNIGHT_MOVE_DELTAS:
            dest_position_name = utils.create_square_name(
                current_position[0] + file_delta, current_position[1] + rank_delta
            )
            if not game.check_square_occupied(
                dest_position_name
            ) or game.check_2_squares_hold_enemies(
                dest_position_name, current_position_name
            ):
                moves.add(dest_position_name)

        return moves


@dataclass
class PieceBishop(Piece):
    """piece bishop"""

    piece_type: utils.PieceType = utils.PieceType.BISHOP

    def calculate_available_moves(
        self, current_position: tuple[int, int], game: GameInterface
    ) -> set[str]:
        current_position_name = utils.create_square_name(*current_position)

        total_iterations = 0  # max 4
        moves: set[str] = set()
        rank_delta = 1
        file_delta = 1
        delta_counter = 0

        while total_iterations < 4:
            delta_counter += 1
            dest_position_name = utils.create_square_name(
                current_position[0] + file_delta * delta_counter,
                current_position[1] + rank_delta * delta_counter,
            )

            square_occupied = game.check_square_occupied(dest_position_name)
            two_squares_hold_enemies = game.check_2_squares_hold_enemies(
                dest_position_name, current_position_name
            )

            if not square_occupied or two_squares_hold_enemies:
                moves.add(dest_position_name)

            if square_occupied:
                delta_counter = 0
                total_iterations += 1
                rank_delta = -rank_delta
                file_delta = -file_delta
                if total_iterations == 2:
                    rank_delta = -1
                    file_delta = 1

        return moves


@dataclass
class PieceRook(Piece):
    """piece rook"""

    piece_type: utils.PieceType = utils.PieceType.ROOK

    def calculate_available_moves(
        self, current_position: tuple[int, int], game: GameInterface
    ) -> set[str]:
        moves: set[str] = set()
        rank_delta = 0
        file_delta = 1
        total_iterations = 0  # at most 4
        current_position_name = utils.create_square_name(*current_position)
        deltal_counter = 0

        while total_iterations < 4:
            deltal_counter += 1

            dest_position_name = utils.create_square_name(
                current_position[0] + deltal_counter * file_delta,
                current_position[1] + deltal_counter * rank_delta,
            )

            square_occupied = game.check_square_occupied(dest_position_name)
            two_squares_hold_enemies = game.check_2_squares_hold_enemies(
                dest_position_name, current_position_name
            )

            if not square_occupied or two_squares_hold_enemies:
                moves.add(dest_position_name)

            if square_occupied:
                deltal_counter = 0
                if file_delta == 1:
                    file_delta = -1
                elif file_delta == -1:
                    file_delta = 0
                    rank_delta = 1
                elif rank_delta == 1:
                    rank_delta = -1
                total_iterations += 1

        return moves


@dataclass
class PieceQueen(Piece):
    """piece queen"""

    piece_type: utils.PieceType = utils.PieceType.QUEEN

    def calculate_available_moves(
        self, current_position: tuple[int, int], game: GameInterface
    ) -> set[str]:
        moves1 = PieceBishop.calculate_available_moves(self, current_position, game)
        moves2 = PieceRook.calculate_available_moves(self, current_position, game)

        return moves1.union(moves2)


KING_MOVE_DELTAS = [
    [1, 1],
    [-1, -1],
    [1, 0],
    [0, 1],
    [-1, 0],
    [0, -1],
    [-1, 1],
    [1, -1],
]


@dataclass
class PieceKing(Piece):
    """piece king"""

    piece_type: utils.PieceType = utils.PieceType.KING

    def calculate_available_moves(
        self, current_position: tuple[int, int], game: GameInterface
    ) -> set[str]:
        current_position_name = utils.create_square_name(*current_position)

        moves: set[str] = set()

        for file_delta, rank_delta in KING_MOVE_DELTAS:
            dest_position_name = utils.create_square_name(
                current_position[0] + file_delta, current_position[1] + rank_delta
            )
            if not game.check_square_occupied(
                dest_position_name
            ) or game.check_2_squares_hold_enemies(
                dest_position_name, current_position_name
            ):
                moves.add(dest_position_name)

        return moves
