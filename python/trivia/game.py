from typing import List
from .igame import IGame

class Player:
    def __init__(self, name: str):
        self.name = name

class Game(IGame):
    BOARD_SIZE = 12
    WINNING_COINS = 6

    def __init__(self):
        self.players = []
        self.positions = [0] * 6
        self.coins = [0] * 6
        self.in_penalty_box = [False] * 6

        self.pop_questions = []
        self.science_questions = []
        self.sports_questions = []
        self.rock_questions = []

        self.current_player = 0
        self.is_getting_out_of_penalty_box = False

        for i in range(50):
            self.pop_questions.append(f"Pop Question {i}")
            self.science_questions.append(f"Science Question {i}")
            self.sports_questions.append(f"Sports Question {i}")
            self.rock_questions.append(self.create_rock_question(i))

    def create_rock_question(self, index: int) -> str:
        return f"Rock Question {index}"

    def has_enough_players(self) -> bool:
        return self.how_many_players() >= 2

    def add(self, player_name: str) -> bool:
        self.positions[self.how_many_players()] = 1
        self.coins[self.how_many_players()] = 0
        self.in_penalty_box[self.how_many_players()] = False
        self.players.append(Player(player_name))

        print(f"{player_name} was added")
        print(f"They are player number {len(self.players)}")
        return True

    def how_many_players(self) -> int:
        return len(self.players)

    def roll(self, roll: int) -> None:
        print(f"{self.players[self.current_player].name} is the current player")
        print(f"They have rolled a {roll}")

        if self.in_penalty_box[self.current_player]:
            if roll % 2 != 0:
                self.is_getting_out_of_penalty_box = True
                print(f"{self.players[self.current_player].name} is getting out of the penalty box")
                self._move_player_and_ask_question(roll)
            else:
                print(f"{self.players[self.current_player].name} is not getting out of the penalty box")
                self.is_getting_out_of_penalty_box = False
        else:
            self._move_player_and_ask_question(roll)

    def _move_player_and_ask_question(self, roll: int) -> None:
        self.positions[self.current_player] = self.positions[self.current_player] + roll
        if self.positions[self.current_player] > self.BOARD_SIZE:
            self.positions[self.current_player] = self.positions[self.current_player] - self.BOARD_SIZE

        print(f"{self.players[self.current_player].name}'s new location is {self.positions[self.current_player]}")
        print(f"The category is {self.current_category()}")
        self.ask_question()

    def ask_question(self) -> None:
        if self.current_category() == "Pop":
            print(self.pop_questions.pop(0))
        if self.current_category() == "Science":
            print(self.science_questions.pop(0))
        if self.current_category() == "Sports":
            print(self.sports_questions.pop(0))
        if self.current_category() == "Rock":
            print(self.rock_questions.pop(0))

    def current_category(self) -> str:
        if self.positions[self.current_player] - 1 == 0: return "Pop"
        if self.positions[self.current_player] - 1 == 4: return "Pop"
        if self.positions[self.current_player] - 1 == 8: return "Pop"
        if self.positions[self.current_player] - 1 == 1: return "Science"
        if self.positions[self.current_player] - 1 == 5: return "Science"
        if self.positions[self.current_player] - 1 == 9: return "Science"
        if self.positions[self.current_player] - 1 == 2: return "Sports"
        if self.positions[self.current_player] - 1 == 6: return "Sports"
        if self.positions[self.current_player] - 1 == 10: return "Sports"
        return "Rock"

    def handle_correct_answer(self) -> bool:
        if self.in_penalty_box[self.current_player]:
            if self.is_getting_out_of_penalty_box:
                print("Answer was correct!!!!")
                self.coins[self.current_player] += 1
                print(f"{self.players[self.current_player].name} now has {self.coins[self.current_player]} Gold Coins.")

                winner = self.did_player_win()
                self._next_player()

                return winner
            else:
                self._next_player()
                return True
        else:
            print("Answer was corrent!!!!")
            self.coins[self.current_player] += 1
            print(f"{self.players[self.current_player].name} now has {self.coins[self.current_player]} Gold Coins.")

            winner = self.did_player_win()
            self._next_player()

            return winner

    def wrong_answer(self) -> bool:
        print("Question was incorrectly answered")
        print(f"{self.players[self.current_player].name} was sent to the penalty box")
        self.in_penalty_box[self.current_player] = True

        self._next_player()
        return True

    def _next_player(self) -> None:
        self.current_player += 1
        if self.current_player == len(self.players):
            self.current_player = 0

    def did_player_win(self) -> bool:
        return not (self.coins[self.current_player] == self.WINNING_COINS)
