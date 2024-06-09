from enum import Enum


def create_square_name(file_: int, rank: int) -> str:
    """
    E.g
    `file_` = 'A', `rank' = 1, => "A1"
    """
    return f"{chr(file_)}{rank}"


class Color(Enum):
    """color enum for game"""

    BLACK = "#C06828"
    WHITE = "#E9E9E9"
    GREEN = "#19992A"


def calculate_color(file_: int, rank: int) -> Color:
    """
    Returns `Color.BLACK` for black, `Color.WHITE` for white
    """
    if (file_ + rank) & 1 == 0:
        return Color.WHITE
    return Color.BLACK


class PieceType(Enum):
    """piece types for game"""

    PAWN = 0
    KNIGHT = 1
    BISHOP = 2
    ROOK = 3
    QUEEN = 4
    KING = 5


MIN_FILE = 65  # 'A'
MAX_FILE = 72  # 'H'

File_A = ord("A")
File_B = ord("B")
File_C = ord("C")
File_D = ord("D")
File_E = ord("E")
File_F = ord("F")
File_G = ord("G")
File_H = ord("H")


def is_file_within_board(file_: int) -> bool:
    """check if given file is within board"""
    return MIN_FILE <= file_ <= MAX_FILE


FILES = [File_A, File_B, File_C, File_D, File_E, File_F, File_G, File_H]


Rank_1 = 1
Rank_2 = 2
Rank_3 = 3
Rank_4 = 4
Rank_5 = 5
Rank_6 = 6
Rank_7 = 7
Rank_8 = 8


def is_rank_within_board(rank: int) -> bool:
    """check if given rank is within board"""
    return Rank_1 <= rank <= Rank_8


def are_rank_and_file_within_board(file: int, rank: int) -> bool:
    """check if given rank and file are within board"""
    return is_file_within_board(file) and is_rank_within_board(rank)


RANKS = [Rank_1, Rank_2, Rank_3, Rank_4, Rank_5, Rank_6, Rank_7, Rank_8]

# colors of squares
SQUARES_COLOR_MAP = {
    create_square_name(file_, rank): calculate_color(file_, rank).value
    for file_ in FILES
    for rank in RANKS
}

SCREEN_DIMENSION = 640
SQUARE_SIZE = 80
NUMBER_OF_HORIZONTAL_CELLS = 8
NUMBER_OF_VERTICAL_CELLS = 8


class PiecePath(Enum):
    """enum for piece images"""

    BLACK_KING = "./images/black_king.png"
    WHITE_KING = "./images/white_king.png"

    BLACK_QUEEN = "./images/black_queen.png"
    WHITE_QUEEN = "./images/white_queen.png"

    BLACK_KNIGHT = "./images/black_knight.png"
    WHITE_KNIGHT = "./images/white_knight.png"

    BLACK_ROOK = "./images/black_rook.png"
    WHITE_ROOK = "./images/white_rook.png"

    BLACK_PAWN = "./images/black_pawn.png"
    WHITE_PAWN = "./images/white_pawn.png"

    BLACK_BISHOP = "./images/black_bishop.png"
    WHITE_BISHOP = "./images/white_bishop.png"


GAME_BOARD = "./images/chess_board.png"


def calculate_image_key(piece_type: PieceType, color: Color) -> str:
    """E.g PAWN, BLACK => BLACK_PAWN"""
    return f"{color.name}_{piece_type.name}"
