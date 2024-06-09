from typing import Optional
from utils import (
    calculate_color,
    create_square_name,
    is_file_within_board,
    is_rank_within_board,
)


class Square:
    def __init__(self, file_: int, rank: int, piece: Optional["Piece"] = None):
        self.__file = file_
        self.__rank = rank
        self.__color = calculate_color(file_, rank)
        self.__piece = piece
        self.__isWithinBoard = is_file_within_board(file_) and is_rank_within_board(
            rank
        )
        self.__name = create_square_name(file_, rank)

    def isWithinBoard(self):
        return self.__isWithinBoard

    def setPiece(self, piece: Optional["Piece"]):
        self.__piece = piece

    def getPiece(self):
        return self.__piece

    def __str__(self):
        return self.__name

    def getRank(self):
        return self.__rank

    def getFile(self):
        return self.__file
