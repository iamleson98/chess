from abc import abstractmethod, ABC
from typing import Optional, Any


class GameInterface(ABC):
    """Abstract base class for game"""

    @abstractmethod
    def switch_turn(self) -> None:
        pass

    @abstractmethod
    def get_board(self) -> dict[str, Optional[Any]]:
        pass

    @abstractmethod
    def check_2_cells_hold_enemies(
        self, square_name_1: str, square_name_2: str
    ) -> bool:
        pass

    @abstractmethod
    def check_square_occupied(self, square_name: str) -> bool:
        pass
