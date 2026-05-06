from typing import List
from .igame import IGame

class Game(IGame):
    def __init__(self):
        self.players = []
        self.positions = [0] * 6
        self.purses = [0] * 6
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

    def is_playable(self) -> bool:
        return self.how_many_players() >= 2

    def add(self, player_name: str) -> bool:
        self.positions[self.how_many_players()] = 1
        self.purses[self.how_many_players()] = 0
        self.in_penalty_box[self.how_many_players()] = False
        self.players.append(player_name)

        print(f"{player_name} was added")
        print(f"They are player number {len(self.players)}")
        return True

    def how_many_players(self) -> int:
        return len(self.players)

    def roll(self, roll: int) -> None:
        print(f"{self.players[self.current_player]} is the current player")
        print(f"They have rolled a {roll}")

        if self.in_penalty_box[self.current_player]:
            if roll % 2 != 0:
                self.is_getting_out_of_penalty_box = True
                print(f"{self.players[self.current_player]} is getting out of the penalty box")
                self.positions[self.current_player] = self.positions[self.current_player] + roll
                if self.positions[self.current_player] > 12:
                    self.positions[self.current_player] = self.positions[self.current_player] - 12

                print(f"{self.players[self.current_player]}'s new location is {self.positions[self.current_player]}")
                print(f"The category is {self.current_category()}")
                self.ask_question()
            else:
                print(f"{self.players[self.current_player]} is not getting out of the penalty box")
                self.is_getting_out_of_penalty_box = False
        else:
            self.positions[self.current_player] = self.positions[self.current_player] + roll
            if self.positions[self.current_player] > 12:
                self.positions[self.current_player] = self.positions[self.current_player] - 12

            print(f"{self.players[self.current_player]}'s new location is {self.positions[self.current_player]}")
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
                self.purses[self.current_player] += 1
                print(f"{self.players[self.current_player]} now has {self.purses[self.current_player]} Gold Coins.")

                winner = self.did_player_win()
                self.current_player += 1
                if self.current_player == len(self.players):
                    self.current_player = 0

                return winner
            else:
                self.current_player += 1
                if self.current_player == len(self.players):
                    self.current_player = 0
                return True
        else:
            print("Answer was corrent!!!!")
            self.purses[self.current_player] += 1
            print(f"{self.players[self.current_player]} now has {self.purses[self.current_player]} Gold Coins.")

            winner = self.did_player_win()
            self.current_player += 1
            if self.current_player == len(self.players):
                self.current_player = 0

            return winner

    def wrong_answer(self) -> bool:
        print("Question was incorrectly answered")
        print(f"{self.players[self.current_player]} was sent to the penalty box")
        self.in_penalty_box[self.current_player] = True

        self.current_player += 1
        if self.current_player == len(self.players):
            self.current_player = 0
        return True

    def did_player_win(self) -> bool:
        return not (self.purses[self.current_player] == 6)
