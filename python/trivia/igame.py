from abc import ABC, abstractmethod

class IGame(ABC):
    @abstractmethod
    def add(self, player_name: str) -> bool:
        pass

    @abstractmethod
    def roll(self, roll: int) -> None:
        pass

    @abstractmethod
    def handle_correct_answer(self) -> bool:
        pass

    @abstractmethod
    def wrong_answer(self) -> bool:
        pass
